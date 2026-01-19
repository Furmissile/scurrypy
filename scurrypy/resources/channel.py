from dataclasses import dataclass

from .base_resource import BaseResource

from ..parts.channel import EditGuildChannel, CreateThreadFromMessage, EditDMChannel, EditThreadChannel, CreateThreadWithoutMessage
from ..parts.message import MessagePart

from ..models.message import MessageModel, PinnedMessageModel
from ..models.channel import ChannelModel, ThreadMemberModel, ArchivedThreads


@dataclass
class Channel(BaseResource):
    """Represents a Discord guild channel."""

    id: int
    """ID of the channel."""

    async def fetch(self) -> ChannelModel:
        """Fetch the full channel data from Discord.

        Returns:
            (ChannelModel): queried channel
        """
        data = await self._http.request("GET", f"/channels/{self.id}")

        return ChannelModel.from_dict(data)
    
    async def edit(self, params: EditGuildChannel | EditDMChannel | EditThreadChannel) -> ChannelModel:
        """Edit this channel.

        Permissions:
            * `MANAGE_CHANNELS` → required to edit this channel

        Args:
            params (EditGuildChannel): channel fields to edit

        Returns:
            (ChannelModel): updated channel
        """

        data = self._http.request('PATCH', f'/channels/{self.id}', data=params.to_dict())

        return ChannelModel.from_dict(data)
    
    async def delete(self) -> None:
        """Deletes this channel from the server.

        Permissions:
            * `MANAGE_CHANNELS` → required to delete this channel
            * `MANAGE_THREADS` → required to delete a thread
        """
        await self._http.request("DELETE", f"/channels/{self.id}")

    async def fetch_messages(self, limit: int = 50, before: int = None, after: int = None, around: int = None) -> list[MessageModel]:
        """Fetches this channel's messages.

        Permissions:
            * `VIEW_CHANNEL` → required to access channel messages
            * `READ_MESSAGE_HISTORY` → required for user, otherwise no messages are returned

        Args:
            limit (int, optional): Max number of messages to return. Range 1 - 100. Defaults to `50`.
            before (int, optional): get messages before this message ID
            after (int, optional): get messages after this message ID
            around (int, optional): get messages around this message ID

        Returns:
            (list[MessageModel]): queried list of messages
        """
        params = {
            "limit": limit,
            "before": before,
            "after": after,
            "around": around
        }

        data = await self._http.request('GET', f'/channels/{self.id}/messages', params=params)

        return [MessageModel.from_dict(msg) for msg in data]
    
    async def send(self, message: str | MessagePart) -> MessageModel:
        """Send a message to this channel.

        Permissions:
            * `SEND_MESSAGES` → required to create a message in this channel

        Args:
            message (str | MessagePart): content as a string or MessagePart

        Returns:
            (MessageModel): created message
        """
        if isinstance(message, str):
            message = MessagePart(content=message)

        message = message._prepare()

        data = await self._http.request(
            "POST", 
            f"/channels/{self.id}/messages", 
            data=message._prepare().to_dict(),
            files=[fp.path for fp in message.attachments]
        )

        return MessageModel.from_dict(data)
    
    async def create_thread_from_message(self, message_id: int, params: CreateThreadFromMessage) -> ChannelModel:
        """Create a thread from a message.

        Args:
            message_id (int): ID of message to attach thread
            params (CreateThreadFromMessage): fields to create thread

        Returns:
            (ChannelModel): new thread
        """

        data = await self._http.request('POST', f"channels/{self.id}/messages/{message_id}/threads", data=params.to_dict())

        return ChannelModel.from_dict(data)
    
    async def fetch_pins(self, limit: int = 50, before: str = None) -> list[PinnedMessageModel]:
        """Get this channel's pinned messages.

        !!! note
            * Creates a `PUBLIC_THREAD` when called on a `GUILF_TEXT` channel
            * Creates an `ANNOUNCEMENT_THREAD` when called on a `GUILD_ANNOUNCEMENT` channel
        
        !!! warning
            Does not work on a `GUILD_FORUM` channel!

        Permissions:
            * `VIEW_CHANNEL` → required to access pinned messages
            * `READ_MESSAGE_HISTORY` → required for reading pinned messages

        Args:
            before (str, optional): get pinned messages before this ISO8601 timestamp
            limit (int, optional): Max number of pinned messages to return. Range 1 - 50. Defaults to `50`.
        
        Returns:
            (list[PinnedMessage]): queried list of pinned messages
        """
        # Set default limit if user didn't supply one
        params = {
            "limit": limit,
            "before": before
        }

        data = await self._http.request('GET', f'/channels/{self.id}/pins', params=params)

        return [PinnedMessageModel.from_dict(item) for item in data]

    async def create_thread_without_message(self, params: CreateThreadWithoutMessage) -> ChannelModel:
        """Create a thread not connected to an existing message.

        Args:
            params (CreateThreadWithoutMessage): fields to create the thread

        Returns:
            (ChannelModel): new thread
        """

        data = self._http.request('POST', f'/channels/{self.id}/threads', data=params.to_dict())

        return ChannelModel.from_dict(data)

    async def join_thread(self) -> None:
        """Add the bot to this thread.

        !!! important
            Required the thread NOT be archived.
        """
        await self._http.request('PUT', f'/channels/{self.id}/thread-members/@me')
    
    async def add_thread_member(self, user_id: int) -> None:
        """Add a user to this thread.

        Args:
            user_id (int): ID of the user to add
        """
        await self._http.request('PUT', f'/channels/{self.id}/thread-members/{user_id}')

    async def leave_thread(self) -> None:
        """Remove the bot from a thread.

        !!! important
            Required the thread NOT be archived.
        """
        await self._http.request('DELETE', f'/channels/{self.id}/thread-members/@me')
    
    async def remove_thread_member(self, user_id: int) -> None:
        """Remove a user to this thread.

        Args:
            user_id (int): ID of the user to remove
        """
        await self._http.request('DELETE', f'/channels/{self.id}/thread-members/{user_id}')

    async def fetch_thread_member(self, user_id: int, with_member: bool = False) -> ThreadMemberModel:
        """Fetch a thread emmber of the specified user ID from this thread.

        Args:
            user_id (int): ID of the user to fetch
            with_member (bool, optional): whether to include the member object. Defaults to `False`.
        
        Returns:
            (ThreadMemberModel): queried thread member
        """

        params = { 'with_member': with_member }

        data = await self._http.request('GET', f'/channels/{self.id}/thread-members/{user_id}', params=params)

        return ThreadMemberModel.from_dict(data)
    
    async def fetch_thread_members(self, limit: int = 100, after: int = None, with_member: bool = False) -> list[ThreadMemberModel]:
        """Fetch all members of this thread.

        !!! warning
            Requires the `GUILD_MEMBERS` privileged intent to use!

        Args:
            limit (int, optional): Max number of thread members to return. Range 0 - 100. Defaults to `100`.
            after (int, optional): members after this user ID
            with_member (bool, optional): whether to include the member object. Defaults to `False`.

        Returns:
            (list[ThreadMemberModel]): queried list of thread members
        """

        params = {
            'with_member': with_member,
            'after': after,
            'limit': limit
        }

        data = await self._http.request('GET', f"/channels/{self.id}/thread-members", params=params)

        return [ThreadMemberModel.from_dict(n) for n in data]

    async def fetch_public_archived_threads(self, before: str = None, limit: int = None) -> ArchivedThreads:
        """Return public archived threads in this channel.

        !!! note
            Threads are ordered by `active_timestamp` in descending order.

        Permissions:
            * `READ_MESSAGE_HISTORY` → required for reading threads

        Args:
            before (str, optional): threads before this timestamp
            limit (int, optional): max number of threads to return

        Returns:
            (ArchivedThreads): queried archived threads
        """

        params = {
            'before': before,
            'limit': limit
        }

        data = await self._http.request('GET', f'/channels/{self.id}/threads/archived/public', params=params)

        return ArchivedThreads.from_dict(data)

    async def fetch_private_archived_threads(self, before: str = None, limit: int = None) -> ArchivedThreads:
        """Return private archived threads in this channel.

        !!! note
            Threads are ordered by `active_timestamp` in descending order.

        Permissions:
            * `READ_MESSAGE_HISTORY` → required for reading threads
            * `MANAGE_THREADS` → required for accessing threads

        Args:
            before (str, optional): threads before this timestamp
            limit (int, optional): max number of threads to return

        Returns:
            (ArchivedThreads): queried archived threads
        """

        params = {
            'before': before,
            'limit': limit
        }

        data = await self._http.request('GET', f'/channels/{self.id}/threads/archived/private', params=params)

        return ArchivedThreads.from_dict(data)

    async def fetch_joined_private_archived_threads(self, before: int = None, limit: int = None) -> ArchivedThreads:
        """Return private archived threads in this channel that the bot has joined.

        !!! note
            Threads are ordered by their ID in descending order.

        Permissions:
            * `READ_MESSAGE_HISTORY` → required for reading threads

        Args:
            before (int, optional): threads before this ID
            after (int, optional): threads after this ID

        Returns:
            (ArchivedThreads): queried archived threads
        """

        params = {
            'before': before,
            'limit': limit
        }

        data = await self._http.request('GET', f'/channels/{self.id}/users/@me/threads/archived/private', params=params)

        return ArchivedThreads.from_dict(data)

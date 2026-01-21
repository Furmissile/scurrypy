from dataclasses import dataclass
from typing import Unpack

from .base_resource import BaseResource

from ..models.message import MessageModel, PinnedMessageModel
from ..models.channel import ChannelModel, ThreadMemberModel

from ..parts.message import MessagePart
from ..parts.channel import ThreadFromMessagePart, ThreadWithoutMessagePart

from ..params.channel import EditGuildChannelParams, EditThreadChannelParams

@dataclass
class Channel(BaseResource):
    """Represents a Discord channel."""

    id: int
    """ID of the channel."""

    async def fetch(self) -> ChannelModel:
        """Fetch the full channel data from Discord.

        Returns:
            (ChannelModel): queried channel
        """
        data = await self._http.request("GET", f"/channels/{self.id}")

        return ChannelModel.from_dict(data)
    
    async def delete(self) -> None:
        """Deletes this channel from the server.

        !!! important "Permissions"
            Requires `MANAGE_CHANNELS` and `MANAGE_THREADS`
        """
        await self._http.request("DELETE", f"/channels/{self.id}")

    async def fetch_messages(self, limit: int = 50, before: int = None, after: int = None, around: int = None) -> list[MessageModel]:
        """Fetches this channel's messages.

        !!! important "Permissions"
            Requires `VIEW_CHANNEL` and `READ_MESSAGE_HISTORY`

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

        !!! important "Permissions"
            Requires `SEND_MESSAGES`

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
    
    async def fetch_pins(self, limit: int = 50, before: str = None) -> list[PinnedMessageModel]:
        """Get this channel's pinned messages.

        !!! important "Permissions"
            Requires `VIEW_CHANNEL` and `READ_MESSAGE_HISTORY`
            
        !!! note
            * Creates a `PUBLIC_THREAD` when called on a `GUILD_TEXT` channel
            * Creates an `ANNOUNCEMENT_THREAD` when called on a `GUILD_ANNOUNCEMENT` channel
        
        !!! warning
            Does not work on a `GUILD_FORUM` channel!

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

@dataclass
class GuildChannel(Channel):
    """Represents a Discord guild channel."""

    async def edit(self, **options: Unpack[EditGuildChannelParams]) -> ChannelModel:
        """Edit this channel.

        !!! important "Permissions"
            Requires `MANAGE_CHANNELS`

        Args:
            options (EditGuildChannelParams): channel fields to edit

        Returns:
            (ChannelModel): updated channel
        """

        if options.get('default_reaction_emoji'):
            options['default_reaction_emoji'] = options['default_reaction_emoji'].to_dict()

        if options.get('available_tags'):
            options['available_tags'] = [i.to_dict() for i in options['available_tags']]

        data = await self._http.request('PATCH', f'/channels/{self.id}', data=options)

        return ChannelModel.from_dict(data)

@dataclass
class ThreadChannel(Channel):
    """Represents a thread channel."""

    async def fetch_member(self, user_id: int, with_member: bool = False) -> ThreadMemberModel:
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
    
    async def fetch_members(self, limit: int = 100, after: int = None, with_member: bool = False) -> list[ThreadMemberModel]:
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

    async def create_from_message(self, message_id: int, thread: ThreadFromMessagePart) -> ChannelModel:
        """Create a thread from a message (attached to the message).

        Args:
            message_id (int): ID of the message to attach the thread
            thread (ThreadFromMessagePart): thread to attach

        Returns:
            ChannelModel: new thread
        """

        data = await self._http.request('POST', f"channels/{self.id}/messages/{message_id}/threads", data=thread.to_dict())

        return ChannelModel.from_dict(data)

    async def create_without_message(self, thread: ThreadWithoutMessagePart) -> ChannelModel:
        """Create a thread not connected to an existing message.

        Args:
            thread (ThreadWithoutMessagePart): thread to create

        Returns:
            ChannelModel: new thread
        """

        data = await self._http.request('POST', f'/channels/{self.id}/threads', data=thread.to_dict())

        return ChannelModel.from_dict(data)
    
    async def edit(self, **options: Unpack[EditThreadChannelParams]) -> ChannelModel:
        """Edit this channel.

        !!! important "Permissions"
            Requires `MANAGE_CHANNELS`

        Args:
            options (EditThreadChannelParams): channel fields to edit

        Returns:
            (ChannelModel): updated channel
        """

        data = await self._http.request('PATCH', f'/channels/{self.id}', data=options)

        return ChannelModel.from_dict(data)

    async def join(self) -> None:
        """Add the bot to this thread.

        !!! important
            Required the thread NOT be archived.
        """
        await self._http.request('PUT', f'/channels/{self.id}/thread-members/@me')
    
    async def leave(self) -> None:
        """Remove the bot from a thread.

        !!! important
            Required the thread NOT be archived.
        """
        await self._http.request('DELETE', f'/channels/{self.id}/thread-members/@me')
    
    async def add_member(self, user_id: int) -> None:
        """Add a user to this thread.

        Args:
            user_id (int): ID of the user to add
        """
        await self._http.request('PUT', f'/channels/{self.id}/thread-members/{user_id}')

    async def remove_member(self, user_id: int) -> None:
        """Remove a user to this thread.

        Args:
            user_id (int): ID of the user to remove
        """
        await self._http.request('DELETE', f'/channels/{self.id}/thread-members/{user_id}')


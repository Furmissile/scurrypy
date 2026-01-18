from dataclasses import dataclass
from typing import Literal

from .base_resource import BaseResource

from ..parts.channel import GuildChannel
from ..parts.message import MessagePart
from ..parts.channel import GuildChannel

from ..models.message import MessageModel
from ..models.channel import ChannelModel, PinnedMessageModel


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
    
    async def edit(self, channel: GuildChannel) -> ChannelModel:
        """Edit this channel.

        Permissions:
            * `MANAGE_CHANNELS` → required to edit this channel

        Args:
            channel (GuildChannel): channel fields to edit

        Returns:
            (ChannelModel): updated channel
        """

        data = self._http.request('PATCH', f'/channels/{self.id}', data=channel.to_dict())

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
    
    async def create_thread_from_message(self, 
        message_id: int, 
        name: str, 
        auto_archive_duration: Literal[60, 1440, 4320, 10080] = None, 
        rate_limit_per_user: int = None
    ) -> ChannelModel:
        """Create a thread from this message.

        Args:
            message_id (int): ID of message to attach thread
            name (str): thread name
            auto_archive_duration (int, optional): time (minutes) of inactivity before thread is archived
            rate_limit_per_user (int, optional): time (seconds) user waits before sending another message

        Returns:
            (ChannelModel): updated channel
        """

        content = {
            'name': name, 
            'auto_archive_duration': auto_archive_duration,
            'rate_limit_per_user': rate_limit_per_user
        }

        data = await self._http.request('POST', f"channels/{self.id}/messages/{message_id}/threads", data=content)

        return ChannelModel.from_dict(data)
    
    async def fetch_pins(self, limit: int = 50, before: str = None) -> list[PinnedMessageModel]:
        """Get this channel's pinned messages.

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

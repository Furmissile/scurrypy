from dataclasses import dataclass
from typing import Optional

from ..core.http import HTTPClient
from ..core.model import DataModel

from ..models import UserModel, EmojiModel
from ..parts.message import MessagePart

@dataclass
class Message(DataModel):
    """A Discord message."""

    id: int
    """ID of the message"""

    channel_id: int
    """Channel ID of the message."""

    _http: HTTPClient
    """HTTP session for requests."""

    author: UserModel = None
    """User data of author of the message."""
    
    content: str = None
    """Content of the message."""

    pinned: bool = None
    """If the message is pinned."""

    type: int = None
    """Type of message."""

    webhook_id: Optional[int] = None
    """ID of the webhook if the message is a webhook."""

    def _update(self, data: dict):
        """Update this message in place."""
        self.__dict__.update(Message.from_dict(data, self._http).__dict__)

    async def fetch(self):
        """Fetches the message data based on the given channel ID and message id.

        Returns:
            (Message): the message object
        """
        data = await self._http.request('GET', f"/channels/{self.channel_id}/messages/{self.id}")

        return Message.from_dict(data, self._http)

    async def send(self, message: str | MessagePart):
        """Sends a new message to the current channel.

        Permissions:
            * SEND_MESSAGES → required to senf your own messages

        Args:
            message (str | MessagePart): can be just text or the MessagePart for dynamic messages

        Returns:
            (Message): the new Message object with all fields populated
        """
        if isinstance(message, str):
            message = MessagePart(content=message)

        data = await self._http.request(
            "POST",
            f"/channels/{self.channel_id}/messages",
            data=message.to_dict(),
            files=[fp.path for fp in message.attachments] if message.attachments else None
        )
        return Message.from_dict(data, self._http)

    async def edit(self, message: str | MessagePart):
        """Edits this message.

        Permissions:
            * MANAGE_MESSAGES → ONLY if editing another user's message

        Args:
            message (str | MessagePart): can be just text or the MessagePart for dynamic messages
        """
        if isinstance(message, str):
            message = MessagePart(content=message)

        data = await self._http.request(
            "PATCH", 
            f"/channels/{self.channel_id}/messages/{self.id}", 
            data=message.to_dict(),
            files=[fp.path for fp in message.attachments] if message.attachments else None)

        self._update(data)

    async def reply(self, message: str | MessagePart):
        """Reply to this message with a new message.

        Permissions:
            * SEND_MESSAGES → required to send the message

        Args:
            message (str | MessagePart): the new message
        """
        if isinstance(message, str):
            message = MessagePart(content=message)

        message = message._set_reference(self.id, self.channel_id)

        await self._http.request(
            'POST', 
            f"/channels/{self.channel_id}/messages",
            data=message.to_dict(),
            files=[fp.path for fp in message.attachments] if message.attachments else None)

    async def crosspost(self):
        """Crosspost this message in an Annoucement channel to all following channels.

        Permissions:
            * SEND_MESSAGES → required to publish your own messages
            * MANAGE_MESSAGES → required to publish messages from others

        Returns:
            (Message): the published (crossposted) message
        """
        data = await self._http.request('POST', f'/channels/{self.channel_id}/messages/{self.id}/crosspost')

        return Message.from_dict(data, self._http)

    async def delete(self):
        """Deletes this message."""
        await self._http.request("DELETE", f"/channels/{self.channel_id}/messages/{self.id}")

    async def add_reaction(self, emoji: EmojiModel | str):
        """Add a reaction from this message.

        Permissions:
            * READ_MESSAGE_HISTORY → required to view message
            * ADD_REACTIONS → required to create reaction

        Args:
            emoji (EmojiModel | str): the standard emoji (str) or custom emoji (EmojiModel)
        """
        if isinstance(emoji, str):
            emoji = EmojiModel(emoji)

        await self._http.request(
            "PUT",
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji.api_code}/@me")
    
    async def remove_reaction(self, emoji: EmojiModel | str):
        """Remove the bot's reaction from this message.

        Args:
            emoji (EmojiModel | str): the standard emoji (str) or custom emoji (EmojiModel)
        """
        if isinstance(emoji, str):
            emoji = EmojiModel(emoji)

        await self._http.request(
            "DELETE",
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji.api_code}/@me")

    async def remove_user_reaction(self, emoji: EmojiModel | str, user_id: int):
        """Remove a specific user's reaction from this message.

        Permissions:
            * MANAGE_MESSAGES → required to remove another user's reaction

        Args:
            emoji (EmojiModel | str): the standard emoji (str) or custom emoji (EmojiModel)
            user_id (int): user's ID
        """
        if isinstance(emoji, str):
            emoji = EmojiModel(emoji)

        await self._http.request(
            "DELETE",
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji.api_code}/{user_id}")

    async def remove_all_reactions(self):
        """Clear all reactions from this message.

        Permissions:
            * MANAGE_MESSAGES → required to remove all reaction
        """
        await self._http.request(
            "DELETE",
            f"/channels/{self.channel_id}/messages/{self.id}/reactions")

    async def pin(self):
        """Pin this message to its channel's pins."""
        await self._http.request('PUT', f'/channels/{self.channel_id}/messages/pins/{self.id}')

    async def unpin(self):
        """Unpin this message from its channel's pins."""
        await self._http.request('DELETE', f'/channels/{self.channel_id}/messages/pins/{self.id}')

    def _has_prefix(self, prefix: str):
        """Utility function. Checks if this message starts with the given prefix.

        Args:
            prefix (str): the prefix

        Returns:
            (bool): whether the message starts with the prefix
        """
        if not self.content:
            return False
        return self.content.lower().startswith(prefix.lower())

    def _extract_args(self, prefix: str):
        """Utility function. Extracts the args from this message's content.

        Args:
            prefix (str): the prefix

        Returns:
            (list[str] | None): list of args or None if no content
        """
        if not self.content:
            return
        return self.content[len(prefix):].strip().lower().split()

from dataclasses import dataclass

from .base_resource import BaseResource

from ..models.emoji import EmojiModel
from ..models.message import MessageModel

from ..parts.message import MessagePart

@dataclass
class Message(BaseResource):
    """A Discord message."""

    id: int
    """ID of the message"""

    channel_id: int
    """Channel ID of the message."""

    async def fetch(self) -> MessageModel:
        """Fetches the message data based on the given channel ID and message id.

        Returns:
            (MessageModel): queried message
        """
        data = await self._http.request('GET', f"/channels/{self.channel_id}/messages/{self.id}")

        return MessageModel.from_dict(data)

    async def edit(self, message: str | MessagePart) -> MessageModel:
        """Edits this message.

        !!! important "Permissions"
            Requires `MANAGE_MESSAGES` *only* if editing another user's message

        Args:
            message (str | MessagePart): content as a string or MessagePart

        Returns:
            (MessageModel): updated message
        """
        if isinstance(message, str):
            message = MessagePart(content=message)
        elif not message:
            raise ValueError("Missing message.")

        data = await self._http.request(
            "PATCH", 
            f"/channels/{self.channel_id}/messages/{self.id}", 
            data=message._prepare().to_dict(),
            files=[fp.path for fp in message.attachments] if message.attachments else None)

        return MessageModel.from_dict(data)

    async def crosspost(self) -> MessageModel:
        """Crosspost this message in an Annoucement channel to all following channels.

        !!! important "Permissions"
            * `SEND_MESSAGES` → required to publish your own messages
            * `MANAGE_MESSAGES` → required to publish messages from others

        Returns:
            (MessageModel): published (crossposted) message
        """
        data = await self._http.request('POST', f'/channels/{self.channel_id}/messages/{self.id}/crosspost')

        return MessageModel.from_dict(data)

    async def delete(self):
        """Deletes this message."""
        await self._http.request("DELETE", f"/channels/{self.channel_id}/messages/{self.id}")

    async def add_reaction(self, emoji: EmojiModel | str) -> None:
        """Add a reaction to this message.

        !!! important "Permissions"
            Requires `READ_MESSAGE_HISTORY` and `ADD_REACTIONS`

        Args:
            emoji (EmojiModel | str): the standard emoji (str) or custom emoji (EmojiModel)
        """
        if isinstance(emoji, str):
            emoji = EmojiModel(emoji)
        elif not emoji:
            raise ValueError("Missing emoji.")

        await self._http.request(
            "PUT",
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji.api_code}/@me")
    
    async def remove_reaction(self, emoji: EmojiModel | str) -> None:
        """Remove the bot's reaction from this message.

        Args:
            emoji (EmojiModel | str): the standard emoji (str) or custom emoji (EmojiModel)
        """
        if isinstance(emoji, str):
            emoji = EmojiModel(emoji)
        elif not emoji:
            raise ValueError("Missing emoji.")

        await self._http.request(
            "DELETE",
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji.api_code}/@me")

    async def remove_user_reaction(self, emoji: EmojiModel | str, user_id: int) -> None:
        """Remove a specific user's reaction from this message.

        !!! important "Permissions"
            Requires `MANAGE_MESSAGES`

        Args:
            emoji (EmojiModel | str): the standard emoji (str) or custom emoji (EmojiModel)
            user_id (int): user's ID
        """
        if isinstance(emoji, str):
            emoji = EmojiModel(emoji)
        elif not emoji:
            raise ValueError("Missing emoji.")

        await self._http.request(
            "DELETE",
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji.api_code}/{user_id}")

    async def remove_all_reactions(self) -> None:
        """Clear all reactions from this message.

        !!! important "Permissions"
            Requires `MANAGE_MESSAGES`
        """
        await self._http.request(
            "DELETE",
            f"/channels/{self.channel_id}/messages/{self.id}/reactions")

    async def pin(self) -> None:
        """Pin this message to its channel's pins."""
        await self._http.request('PUT', f'/channels/{self.channel_id}/messages/pins/{self.id}')

    async def unpin(self) -> None:
        """Unpin this message from its channel's pins."""
        await self._http.request('DELETE', f'/channels/{self.channel_id}/messages/pins/{self.id}')

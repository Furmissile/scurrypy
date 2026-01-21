from dataclasses import dataclass
from typing import Unpack

from .base_resource import BaseResource

from ..models.emoji import EmojiModel

from ..parts.bot_emoji import BotEmojiPart

from ..params.bot_emoji import EditBotEmojiParams

@dataclass
class BotEmoji(BaseResource):
    """Represents a Discord Bot Emoji."""

    application_id: int
    """Application ID of the emojis."""

    async def fetch(self, emoji_id: int) -> EmojiModel:
        """Fetch an emoji from the bot repository.

        Args:
            emoji_id (int): emoji ID

        Returns:
            (EmojiModel): queried emoji
        """
        data = await self._http.request("GET", f"/applications/{self.application_id}/emojis/{emoji_id}")

        return EmojiModel.from_dict(data)
    
    async def fetch_all(self) -> list[EmojiModel]:
        """Fetch all emojis from the bot repository.

        Returns:
            (list[EmojiModel]): queried list of bot emojis
        """
        data = await self._http.request("GET", f"/applications/{self.application_id}/emojis")

        emojis = data.get("items")

        return [EmojiModel.from_dict(emoji) for emoji in emojis]
    
    async def create(self, emoji: BotEmojiPart) -> EmojiModel:
        """Add an emoji to the bot emoji repository.

        Args:
            emoji (BotEmojiPart): bot emoji fields

        Returns:
            (EmojiModel): new emoji
        """
        data = await self._http.request(
            'POST', 
            f'/applications/{self.application_id}/emojis',
            data=emoji.to_dict()
        )
    
        return EmojiModel.from_dict(data)
    
    async def edit(self, emoji_id: int, **options: Unpack[EditBotEmojiParams]) -> EmojiModel:
        """Edit an emoji in the bot repository.

        Args:
            emoji_id (int): ID of the emoji
            options (EditBotEmojiParams): fields to edit the emoji

        Returns:
            (EmojiModel): updated emoji
        """
        data = await self._http.request(
            'PATCH', 
            f'/applications/{self.application_id}/emojis/{emoji_id}', 
            data=options
        )

        return EmojiModel.from_dict(data)

    async def delete(self, emoji_id: int) -> None:
        """Deletes an emoji from the bot repository.

        Args:
            emoji_id (int): ID of the emoji to remove
        """
        await self._http.request('DELETE', f'/applications/{self.application_id}/emojis/{emoji_id}')

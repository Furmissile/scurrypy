from dataclasses import dataclass
from typing import Unpack

from .base_resource import BaseResource

from ..models.emoji import EmojiModel

from ..parts.guild_emoji import GuildEmojiPart

from ..params.guild_emoji import EditGuildEmojiParams

@dataclass
class GuildEmoji(BaseResource):
    """Represents a Discord Guild Emoji."""

    guild_id: int
    """Guild ID of the emojis."""

    async def fetch(self, emoji_id: int) -> EmojiModel:
        """Fetch an emoji from this guild.

        Args:
            emoji_id (int): emoji ID

        Returns:
            (EmojiModel): queried guild emoji
        """
        data = await self._http.request("GET", f"/guilds/{self.guild_id}/emojis/{emoji_id}")

        return EmojiModel.from_dict(data)
    
    async def fetch_all(self) -> list[EmojiModel]:
        """Fetch all emojis from this guild.

        Returns:
            (list[EmojiModel]): queried list of guild emojis
        """
        data = await self._http.request("GET", f"/guilds/{self.guild_id}/emojis")

        return [EmojiModel.from_dict(emoji) for emoji in data]

    async def create(self, emoji: GuildEmojiPart) -> EmojiModel:
        """Create a new emoji for this guild.
        Fires [`GuildEmojisUpdateEvent`][scurrypy.events.guild_events.GuildEmojisUpdateEvent].

        Args:
            emoji (GuildEmojiPart): fields for creating a guild emoji

        Returns:
            (EmojiModel): new emoji
        """
        data = await self._http.request(
            'POST', 
            f'/guilds/{self.guild_id}/emojis', 
            data=emoji.to_dict()
        )

        return EmojiModel.from_dict(data)
    
    async def edit(self, emoji_id: int, **options: Unpack[EditGuildEmojiParams]) -> EmojiModel:
        """Edit a guild emoji in this guild.
        Fires [`GuildEmojisUpdateEvent`][scurrypy.events.guild_events.GuildEmojisUpdateEvent].

        Args:
            emoji_id (int): ID of the emoji to edit
            options (EditGuildEmojiParams): params for editing a guild's emoji

        Returns:
            (EmojiModel): updated emoji
        """
        data = await self._http.request(
            'PATCH', 
            f'/guilds/{self.guild_id}/emojis/{emoji_id}', 
            data=options
        )

        return EmojiModel.from_dict(data)

    async def delete(self, emoji_id: int) -> None:
        """Delete an emoji from this guild.
        Fires [`GuildEmojisUpdateEvent`][scurrypy.events.guild_events.GuildEmojisUpdateEvent].

        !!! important "Permissions"
            * `CREATE_GUILD_EXPRESSIONS` → required if created by the current user (or `MANAGE_GUILD_EXPRESSIONS`)
            * `MANAGE_GUILD_EXPRESSIONS` → required for other emojis

        Args:
            emoji_id (int): ID of the emoji
        """
        await self._http.request('DELETE', f'/guilds/{self.guild_id}/emojis/{emoji_id}')

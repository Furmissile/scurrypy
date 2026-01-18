from dataclasses import dataclass

from .base_resource import BaseResource

from ..models.emoji import EmojiModel

from ..parts.image_data import ImageData

@dataclass
class GuildEmoji(BaseResource):
    """Represents a Discord Guild Emoji."""

    guild_id: int
    """Guild ID of the emojis."""

    async def fetch(self, emoji_id: int):
        """Fetch an emoji from this guild.

        Args:
            emoji_id (int): emoji ID

        Returns:
            (EmojiModel): the Emoji object
        """
        data = await self._http.request("GET", f"/guilds/{self.guild_id}/emojis/{emoji_id}")

        return EmojiModel.from_dict(data)
    
    async def fetch_all(self):
        """Fetch all emojis from this guild.

        Returns:
            (list[EmojiModel]): queried guild emojis
        """
        data = await self._http.request("GET", f"/guilds/{self.guild_id}/emojis")

        return [EmojiModel.from_dict(emoji) for emoji in data]

    async def create(self, name: str, image: ImageData, roles: list[int] = None):
        """Create a new emoji for this guild.

        Args:
            name (str): name of the emoji
            image (ImageData): emoji image (128x128)
            roles (list[int]): roles allowed to use this emoji
        """

        data = await self._http.request(
            'POST', 
            f'/guilds/{self.guild_id}/emojis', 
            data={
                'name': name,
                'image': image.uri,
                'roles': roles
            }
        )

        return EmojiModel.from_dict(data)
    
    async def modify(self, emoji_id: int, name: str = None, roles: list[int] = None):
        """Modify a guild emoji in this guild.

        Args:
            emoji_id (int): ID of the emoji to modify
            name (str): new name for the emoji
            roles (list[int]): new roles allowed to use this emoji
        """

        data = await self._http.request(
            'PATCH', 
            f'/guilds/{self.guild_id}/emojis/{emoji_id}', 
            data={
                'name': name,
                'roles': roles
            }
        )

        return EmojiModel.from_dict(data)

    async def delete(self, emoji_id: int):
        """Delete an emoji from this guild.

        Permissions:
            * CREATE_GUILD_EXPRESSIONS → if created by the current user (or `MANAGE_GUILD_EXPRESSIONS`)
            * MANAGE_GUILD_EXPRESSIONS → for other emojis

        Args:
            emoji_id (int): ID of the emoji
        """

        await self._http.request('DELETE', f'/guilds/{self.guild_id}/emojis/{emoji_id}')

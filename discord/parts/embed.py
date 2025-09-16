from dataclasses import dataclass
from typing import Optional
from discord.model import DataModel
from datetime import datetime, timezone
from ..models.user import UserModel

@dataclass
class _EmbedAuthor(DataModel):
    """Embed author parameters."""
    name: str
    url: Optional[str] = None
    icon_url: Optional[str] = None

@dataclass
class _EmbedThumbnail(DataModel):
    """Embed thumbnail."""
    url: str

@dataclass
class _EmbedImage(DataModel):
    """Embed image."""
    url: str

@dataclass
class _EmbedFooter(DataModel):
    """Embed footer."""
    text: str
    url: Optional[str] = None
    icon_url: Optional[str] = None

@dataclass
class _EmbedField(DataModel):
    """Embed field."""
    name: str
    value: str
    inline: Optional[bool] = None

@dataclass
class EmbedBuilder(DataModel):
    """Represents the Embed portion of a message."""

    title: Optional[str] = None
    """This embed's title."""

    description: Optional[str] = None
    """This embed's description."""

    timestamp: Optional[str] = None
    """Timestamp of when the embed was sent."""

    color: Optional[int] = None
    """Embed's accent color."""

    author: Optional[_EmbedAuthor] = None
    """Embed's author."""

    thumbnail: Optional[_EmbedThumbnail] = None
    """Embed's thumbnail attachment."""

    image: Optional[_EmbedImage] = None
    """Embed's image attachment."""

    fields: Optional[list[_EmbedField]] = None
    """List of embed's fields."""

    footer: Optional[_EmbedFooter] = None
    """Embed's footer."""

    def set_color(self, hex: str):
        """Set this embed's color with a hex.

        Args:
            hex (str): color as a hex code (format: #FFFFFF)

        Returns:
            (EmbedBuilder): self
        """
        self.color=int(hex.strip('#'), 16)
        return self
    
    def set_user_author(self, user: UserModel):
        """Set this embed's author.

        Args:
            user (UserModel): the user model

        Returns:
            (EmbedBuilder): self
        """
        self.author = _EmbedAuthor(
            name=user.username,
            icon_url=f"https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.png"
        )
        return self
    
    def set_image(self, url: str):
        """Set this embed's image.

        Args:
            url (str): attachment://<file> scheme or http(s) URL

        Returns:
            (EmbedBuilder): self
        """
        self.image = _EmbedImage(url=url)
        return self
    
    def set_thumbnail(self, url: str):
        """Set this embed's thumbnail.

        Args:
            url (str): attachment://<file> scheme or http(s) URL

        Returns:
            (EmbedBuilder): self
        """
        self.thumbnail = _EmbedThumbnail(url=url)
        return self
    
    def set_footer(self, text: str, icon_url: str = None):
        """Set this embed's footer.

        Args:
            text (str): footer's text
            icon_url (str, optional): attachment://<file> scheme or http(s) URL.

        Returns:
            (EmbedBuilder): self
        """
        self.footer = _EmbedFooter(text=text, icon_url=icon_url)
        return self
    
    def add_field(self, name: str, value: str, is_inline: bool = False):
        """Add a field to this embed.

        Args:
            name (str): field's title
            value (str): field's text
            is_inline (bool): if this field should be inlined

        Returns:
            (EmbedBuilder): self
        """
        self.fields.append(_EmbedField(name=name, value=value, inline=is_inline))
        return self
    
    def set_timestamp(self):
        """Set this embed's timestamp.

        Returns:
            (EmbedBuilder): self
        """
        self.timestamp = datetime.now(timezone.utc).isoformat()
        return self

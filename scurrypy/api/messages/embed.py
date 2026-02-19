from dataclasses import dataclass

from ...core.model import DataModel

from ..user import UserModel

from datetime import datetime, timezone

@dataclass
class EmbedAuthor(DataModel):
    """Represents fields for creating an embed author."""

    name: str = None
    """Name of the author."""

    url: str | None = None
    """URL of the author. http or attachment://<filename> scheme."""

    icon_url: str | None = None
    """URL of author's icon. http or attachment://<filename> scheme."""

@dataclass
class EmbedThumbnail(DataModel):
    """Represents fields for creating an embed thumbnail."""

    url: str | None = None
    """Thumbnail content. http or attachment://<filename> scheme."""

@dataclass
class EmbedField(DataModel):
    """Represents fields for creating an embed field."""

    name: str | None = None
    """Name of the field."""

    value: str | None = None
    """Value of the field."""

    inline: bool | None = False
    """Whether or not this field should display inline. Defaults to `False`."""

@dataclass
class EmbedImage(DataModel):
    """Represents fields for creating an embed image."""

    url: str | None = None
    """Image content. http or attachment://<filename> scheme."""

@dataclass
class EmbedFooter(DataModel):
    """Represents fields for creating an embed footer."""

    text: str | None = None
    """Footer text."""

    icon_url: str | None = None
    """URL of the footer icon. http or attachment://<filename> scheme."""

@dataclass
class Embed(DataModel):
    """Represents fields for creating an embed."""

    title: str | None = None
    """This embed's title."""

    description: str | None = None
    """This embed's description."""

    timestamp: str | None = None
    """Timestamp of when the embed was sent."""

    color: int | None = None
    """Embed's accent color."""

    author: EmbedAuthor | None = None
    """Embed's author."""

    thumbnail: EmbedThumbnail | None = None
    """Embed's thumbnail attachment."""

    image: EmbedImage | None = None
    """Embed's image attachment."""

    fields: list[EmbedField] | None = None
    """List of embed's fields."""

    footer: EmbedFooter | None = None
    """Embed's footer."""

    def set_user_author(self, user: UserModel):
        """Embed author builder.

        Args:
            user (UserModel): user author
        """
        self.author = EmbedAuthor(
            name=user.username,
            icon_url=f"https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.png"
        )

    def set_timestamp(self, datetime: datetime = None):
        """Embed timestamp builder. Adheres to ISO8601 format.

        Args:
            datetime (datetime, optional): datetime object
        """
        dt = dt or datetime.now(timezone.utc)

        self.timestamp = dt.isoformat()

    def to_dict(self):
        from ..components import Thumbnail as V2Thumbnail

        if isinstance(self.thumbnail, V2Thumbnail):
            raise TypeError(
                "EmbedPart.thumbnail received a ComponentV2 Thumbnail.\n"
                "Use scurrypy.EmbedThumbnail(url) for embed thumbnails."
            )
        
        if isinstance(self.image, V2Thumbnail):
            raise TypeError(
                "EmbedPart.image received a ComponentV2 Thumbnail.\n"
                "Use scurrypy.EmbedImage(url) for embed thumbnails."
            )
        
        return super().to_dict()

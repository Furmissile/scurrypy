from dataclasses import dataclass, field
from ..core.model import DataModel

from typing import Optional

@dataclass
class EmbedAuthorPart(DataModel):
    """Represents fields for creating an embed author."""

    name: str = None
    """Name of the author."""

    url: Optional[str] = None
    """URL of the author. http or attachment://<filename> scheme."""

    icon_url: Optional[str] = None
    """URL of author's icon. http or attachment://<filename> scheme."""

@dataclass
class EmbedThumbnailPart(DataModel):
    """Represents fields for creating an embed thumbnail."""

    url: str = None
    """Thumbnail content. http or attachment://<filename> scheme."""

@dataclass
class EmbedFieldPart(DataModel):
    """Represents fields for creating an embed field."""

    name: str = None
    """Name of the field."""

    value: str = None
    """Value of the field."""

    inline: Optional[bool] = False
    """Whether or not this field should display inline. Defaults to `False`."""

@dataclass
class EmbedImagePart(DataModel):
    """Represents fields for creating an embed image."""

    url: str = None
    """Image content. http or attachment://<filename> scheme."""

@dataclass
class EmbedFooterPart(DataModel):
    """Represents fields for creating an embed footer."""

    text: str = None
    """Footer text."""

    icon_url: Optional[str] = None
    """URL of the footer icon. http or attachment://<filename> scheme."""

@dataclass
class EmbedPart(DataModel):
    """Represents fields for creating an embed."""

    title: Optional[str] = None
    """This embed's title."""

    description: Optional[str] = None
    """This embed's description."""

    timestamp: Optional[str] = None
    """Timestamp of when the embed was sent."""

    color: Optional[int] = None
    """Embed's accent color."""

    author: Optional[EmbedAuthorPart] = None
    """Embed's author."""

    thumbnail: Optional[EmbedThumbnailPart] = None
    """Embed's thumbnail attachment."""

    image: Optional[EmbedImagePart] = None
    """Embed's image attachment."""

    fields: Optional[list[EmbedFieldPart]] = field(default_factory=list)
    """List of embed's fields."""

    footer: Optional[EmbedFooterPart] = None
    """Embed's footer."""

    def to_dict(self):
        """
        EXCEPTION to the "models contain no custom methods" rule for two reasons:

        1. `to_dict` already exists on all models via inheritance, so overriding it
        does not break the design model.

        2. `Thumbnail` (Component V2) and `EmbedThumbnail` (Embed-only) are extremely
        easy to confuse. This guard catches the mistake early and provides a clear,
        actionable error instead of allowing Discord to return an obscure 400 error.
        """
        from .components_v2 import ThumbnailPart as V2Thumbnail

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
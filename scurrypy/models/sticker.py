from dataclasses import dataclass
from ..core.model import DataModel

from typing import Optional

from .user import UserModel

@dataclass
class StickerModel(DataModel):
    """Represents the sticker object."""

    id: int
    """ID of the sticker."""

    pack_id: Optional[int]
    """ID of the pack the sticker is from (if standard)."""

    name: str
    """Name of the sticker."""

    description: str
    """Description of the sticker."""

    tags: str
    """Autocomplete/suggestion tags for the sticker."""

    type: int
    """Type of sticker. See [`StickerTypes`][scurrypy.parts.guild.StickerTypes]."""

    format_type: int
    """Type of sticker format. See [`StickerFormatTypes`][scurrypy.parts.guild.StickerFormatTypes]."""

    available: Optional[bool]
    """Whether this guild sticker can be used.
    
    !!! note
        May be `False` due to loss of Server Boosts
    """

    guild_id: Optional[int]
    """ID of the guild that owns this sticker."""
    
    user: Optional[UserModel]
    """The user that uploaded the guild sticker."""

    sort_type: Optional[int]
    """The standard sticker's sort order within its pack."""

@dataclass
class StickerItemModel(DataModel):
    """Represents a minimal sticker item."""
    
    id: int
    """ID of the sticker."""

    name: str
    """Name of the sticker."""

    format_type: int
    """Type of sticker format. See [`StickerFormatTypes`][scurrypy.parts.guild.StickerFormatTypes]."""

@dataclass
class StickerPackModel(DataModel):
    """Represents a pack of standard stickers."""

    id: int
    """ID of the sticker pack."""

    stickers: list[StickerModel]
    """The stickers in the pack."""

    name: str
    """Name of the sticker pack."""

    sku_id: int
    """ID of the pack's SKU."""

    cover_sticker_id: Optional[int]
    """ID of a sticker in the pack which is shown as the pack's icon."""

    description: str
    """Description of the sticker pack."""

    banner_asset_id: Optional[int]
    """ID of the sticker pack's banner image."""

from dataclasses import dataclass

from ...core.model import DataModel
from ...core.snowflake import Snowflake

from ...enums.guild import StickerType, StickerFormatType

from ..user import UserModel

@dataclass
class StickerModel(DataModel):
    """Represents the sticker object."""

    id: Snowflake
    """ID of the sticker."""

    pack_id: Snowflake | None
    """ID of the pack the sticker is from (if standard)."""

    name: str
    """Name of the sticker."""

    description: str
    """Description of the sticker."""

    tags: str
    """Autocomplete/suggestion tags for the sticker."""

    type: StickerType
    """Type of sticker."""

    format_type: StickerFormatType
    """Type of sticker format."""

    available: bool | None
    """Whether this guild sticker can be used.
    
    !!! note
        May be `False` due to loss of Server Boosts
    """

    guild_id: Snowflake | None
    """ID of the guild that owns this sticker."""
    
    user: UserModel | None
    """The user that uploaded the guild sticker."""

    sort_type: int | None
    """The standard sticker's sort order within its pack."""

@dataclass
class StickerItemModel(DataModel):
    """Represents a minimal sticker item."""
    
    id: Snowflake
    """ID of the sticker."""

    name: str
    """Name of the sticker."""

    format_type: StickerFormatType
    """Type of sticker format."""

@dataclass
class StickerPackModel(DataModel):
    """Represents a pack of standard stickers."""

    id: Snowflake
    """ID of the sticker pack."""

    stickers: list[StickerModel]
    """The stickers in the pack."""

    name: str
    """Name of the sticker pack."""

    sku_id: Snowflake
    """ID of the pack's SKU."""

    cover_sticker_id: Snowflake | None
    """ID of a sticker in the pack which is shown as the pack's icon."""

    description: str
    """Description of the sticker pack."""

    banner_asset_id: Snowflake | None
    """ID of the sticker pack's banner image."""

@dataclass
class StickerPart(DataModel):
    """Represents fields for creating a sticker."""

    name: str | None = None
    """Name of the sticker."""

    description: str | None = None
    """Description of the sticker."""

    tags: str | None = None
    """Autocomplete/suggestion tags for the sticker."""

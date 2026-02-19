from dataclasses import dataclass

from ...core.model import DataModel
from ...core.snowflake import Snowflake

@dataclass
class TagModel(DataModel):
    """Represents the tag object found in `GUILD_FORUM` channels."""
    
    id: Snowflake
    """ID of the tag."""

    name: str
    """Name of the tag."""

    moderated: bool
    """Whether the tag can only be added/removed by a member with `MANAGE_THREADS`."""
    
    emoji_id: Snowflake
    """ID of a guild's custom emoji."""
    
    emoji_name: str
    """Unicode character of the emoji."""

@dataclass
class TagPart(DataModel):
    """Represents the tag object found in `GUILD_FORUM` channels."""
    
    name: str = None
    """Name of the tag."""

    moderated: bool = None
    """Whether the tag can only be added/removed by a member with `MANAGE_THREADS`."""
    
    emoji_id: Snowflake = None
    """ID of a guild's custom emoji."""
    
    emoji_name: str = None
    """Unicode character of the emoji."""

from dataclasses import dataclass
from typing import Optional
from ..model import DataModel

# NOTE: Supported Channel Types listed here
class ChannelTypes:
    """Constants for channel types."""
    GUILD_TEXT = 0
    GUILD_CATEGORY = 4
    GUILD_ANNOUNCEMENT = 5

@dataclass
class GuildChannel(DataModel):
    """Parameters for creating/editing a guild channel."""
    name: Optional[str] = None
    type: Optional[int] = None
    topic: Optional[str] = None
    position: Optional[int] = None
    parent_id: Optional[int] = None
    nsfw: Optional[bool] = None

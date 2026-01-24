from dataclasses import dataclass, field
from ..core.model import DataModel

from typing import Optional

@dataclass
class BulkGuildBanPart(DataModel):
    """Represents fields for creating a bulk ban."""

    user_ids: list[int] = field(default_factory=list)
    """List of user IDs to ban. Max `200`."""

    delete_message_seconds: Optional[int] = 0
    """seconds back to delete messages. Max `604800` (7 days). Defaults to `0`."""

@dataclass
class WelcomeScreenChannelPart(DataModel):
    """Represents fields for creating a welcome screen channel."""

    channel_id: int = None
    """ID of the channel to display."""

    description: str = None
    """Description for the channel to display."""

    emoji_id: int = None
    """ID of the emoji (if custom)."""

    emoji_name: str = None
    """Name of the emoji."""

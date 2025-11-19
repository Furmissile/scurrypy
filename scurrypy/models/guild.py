from dataclasses import dataclass
from ..core.model import DataModel

from .emoji import EmojiModel

from typing import Optional

@dataclass
class ReadyGuildModel(DataModel):
    """Guild info from Ready event."""
    id: int
    """ID of the associated guild."""

    unavailable: bool
    """If the guild is offline."""

@dataclass
class GuildModel(DataModel):
    """Represents a Discord guild."""

    id: int
    """ID of the guild."""

    name: str
    """Name of the guild."""

    icon: Optional[str] = None
    """Icon hash of the guild."""

    emojis: list[EmojiModel] = None
    """List of emojis reigstered in the guild."""

    approximate_member_count: Optional[int] = None
    """Approximate member count."""

    description: str = None
    """Description of the guild."""
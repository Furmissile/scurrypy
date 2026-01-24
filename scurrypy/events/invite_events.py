from dataclasses import dataclass
from ..core.model import DataModel
from .base_event import Event

from typing import Optional

from ..models.user import UserModel

@dataclass
class InviteCreateEvent(Event, DataModel):
    """Received when an invite is created."""

    channel_id: int
    """Channel ID in which the invite belongs."""

    code: str
    """Invite code (unique ID)."""

    guild_id: Optional[int]
    """Guild ID in which the invite belongs."""

    inviter: Optional[UserModel]
    """User who created invite."""

    uses: int
    """Number of times this invite was used."""

    max_uses: int
    """Max number of times this invite can be used."""

    max_age: int
    """Duration (in seconds) after which this invite expires."""

    temporary: bool
    """Whether this invite only grants temporary membership."""

    created_at: str
    """ISO8601 timestamp for when this invite was created."""


@dataclass
class InviteDeleteEvent(Event, DataModel):
    """Received when an invite is deleted."""

    channel_id: int
    """Channel ID in which the invite belongs."""

    guild_id: Optional[int]
    """Guild ID in which the invite belongs."""

    code: str
    """Unique invite code."""

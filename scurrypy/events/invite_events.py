from dataclasses import dataclass

from ..core.model import DataModel
from ..core.snowflake import Snowflake

from .base_event import Event

from ..enums.events import EventType

from ..api.user import UserModel

@dataclass
class InviteCreateEvent(Event, DataModel):
    """Received when an invite is created."""

    dispatch_name = EventType.INVITE_CREATE

    channel_id: Snowflake
    """Channel ID in which the invite belongs."""

    code: str
    """Invite code (unique ID)."""

    guild_id: Snowflake | None
    """Guild ID in which the invite belongs."""

    inviter: UserModel | None
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

    dispatch_name = EventType.INVITE_DELETE

    channel_id: Snowflake
    """Channel ID in which the invite belongs."""

    guild_id: Snowflake | None
    """Guild ID in which the invite belongs."""

    code: str
    """Unique invite code."""

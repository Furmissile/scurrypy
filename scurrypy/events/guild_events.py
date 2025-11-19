from dataclasses import dataclass
from ..core.model import DataModel

from ..models import MemberModel
from ..resources.channel import Channel

@dataclass
class GuildEvent(DataModel):
    """Base guild event."""
    
    joined_at: str
    """ISO8601 timestamp of when app joined the guild."""

    large: bool
    """If the guild is considered large."""

    member_count: int
    """Total number of members in the guild."""

    members: list[MemberModel]
    """Users in the guild."""

    channels: list[Channel]
    """Channels in the guild."""

class GuildCreateEvent(GuildEvent):
    """Received when the bot has joined a guild."""
    pass

class GuildUpdateEvent(GuildEvent):
    """Received when a guild has been edited."""
    pass

class GuildDeleteEvent(GuildEvent):
    """Received when the bot has left a guild or the guild was deleted."""
    pass

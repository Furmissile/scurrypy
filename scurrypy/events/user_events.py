from dataclasses import dataclass
from ..core.model import DataModel
from .base_event import Event

from ..models.user import UserModel, GuildMemberModel

@dataclass
class UserUpdateEvent(Event, UserModel):
    """Received when a user's settings are updated."""
    pass

@dataclass
class GuildMemberAddEvent(Event, GuildMemberModel):
    """Received when a member joins a guild the bot is in.

    !!! warning
        Requires privileged `GUILD_MEMBERS` intent.
    """

    guild_id: int
    """ID of the guild."""

@dataclass
class GuildMemberUpdateEvent(Event, DataModel):
    """Received when a guild member is updated.
    
    !!! warning
        Requires privileged `GUILD_MEMBERS` intent.
    """
    guild_id: int
    """ID of the guild."""

    roles: list[int]
    """List of user's roles (their IDs)."""

    user: UserModel
    """The User object."""

    avatar: str
    """Guild avatar hash."""

    banner: str
    """Guild banner hash."""

    joined_at: str
    """When the user joined the guild"""

@dataclass
class GuildMemberRemoveEvent(Event, DataModel):
    """Received when a member leaves or is kicked/banned from a guild the bot is in.
    
    !!! warning
        Requires privileged `GUILD_MEMBERS` intent.
    """

    guild_id: int
    """ID of the guild."""

    user: UserModel
    """User object of the user leaving the guild."""

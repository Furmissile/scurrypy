from dataclasses import dataclass
from ..core.model import DataModel

from typing import Optional

class GuildMemberFlags:
    DID_REJOIN = 1 << 0
    COMPLETED_ONBOARDING = 1 << 1
    BYPASSES_VERIFICATION = 1 << 2
    STARTED_ONBOARDING = 1 << 3
    STARTED_HOME_ACTIONS = 1 << 5
    COMPLETED_HOME_ACTIONS = 1 << 6
    AUTOMOD_QUARANTINED_USERNAME = 1 << 7
    AUTOMOD_QUARANTINED_TAG = 1 << 8

@dataclass
class UserModel(DataModel):
    """Represents the User object."""

    id: int
    """ID of the user."""

    username: str
    """Username of the user."""

    discriminator: str
    """Discriminator of the user (#XXXX)"""

    global_name: str
    """Global name of the user."""

    avatar: str
    """Image hash of the user's avatar."""

    bot: Optional[bool]
    """If the user is a bot."""

    system: Optional[bool]
    """If the user belongs to an OAuth2 application."""

    mfa_enabled: Optional[bool]
    """Whether the user has two factor enabled."""

    banner: Optional[str]
    """Image hash of the user's banner."""

    accent_color: Optional[int]
    """Color of user's banner represented as an integer."""

    locale: Optional[str]
    """Chosen language option of the user."""

@dataclass
class GuildMemberModel(DataModel):
    """Represents a guild member."""

    roles: list[int]
    """List of roles registered to the guild member."""

    user: UserModel
    """User data associated with the guild member."""

    nick: str
    """Server nickname of the guild member."""

    avatar: str
    """Server avatar hash of the guild mmeber."""

    joined_at: str
    """ISO8601 timestamp of when the guild member joined server."""

    permissions: Optional[int]
    """Total permissions of the member in the channel, including overwrites, 
        returned when in the interaction object. [`INT_LIMIT`]
    """

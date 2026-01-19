from dataclasses import dataclass
from ..core.model import DataModel

from typing import Optional

@dataclass
class UserModel(DataModel):
    """Describes the User object."""

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

    deaf: bool
    """If the member is deaf in a VC (input)."""

    mute: bool
    """If the member is muted in VC (output)."""

    permissions: Optional[int]
    """Total permissions of the member in the channel, including overwrites, 
        returned when in the interaction object. [`INT_LIMIT`]
    """

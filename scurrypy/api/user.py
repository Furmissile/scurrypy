from dataclasses import dataclass

from ..core.model import DataModel
from ..core.snowflake import Snowflake

from ..enums.permissions import Permissions

@dataclass
class UserModel(DataModel):
    """Represents the User object."""

    id: Snowflake
    """ID of the user."""

    username: str
    """Username of the user."""

    discriminator: str
    """Discriminator of the user (#XXXX)"""

    global_name: str
    """Global name of the user."""

    avatar: str
    """Image hash of the user's avatar."""

    bot: bool | None
    """If the user is a bot."""

    banner: str | None
    """Image hash of the user's banner."""

    accent_color: int | None
    """Color of user's banner represented as an integer."""

    locale: str | None
    """Chosen language option of the user."""

@dataclass
class GuildMemberModel(DataModel):
    """Represents a guild member."""

    roles: list[Snowflake]
    """List of roles registered to the guild member."""

    user: UserModel
    """User data associated with the guild member."""

    nick: str
    """Server nickname of the guild member."""

    avatar: str
    """Server avatar hash of the guild mmeber."""

    joined_at: str
    """ISO8601 timestamp of when the guild member joined server."""

    permissions: Permissions | None
    """Total permissions of the member in the channel, including overwrites, 
        returned when in the interaction object. [`INT_LIMIT`]
    """

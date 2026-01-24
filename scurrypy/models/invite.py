from dataclasses import dataclass
from ..core.model import DataModel

from typing import Optional

from .guild import GuildModel
from .channel import ChannelModel
from .user import UserModel
from .role import RoleModel

class InviteTypes:
    GUILD = 0
    GROUP_DM = 1
    FRIEND = 2

@dataclass
class InviteModel(DataModel):
    """Represents a code that adds a user to guild or group DM channel."""

    type: int
    """Type of invite. See [`InviteTypes`][scurrypy.models.invite.InviteTypes]."""

    code: str
    """Invite code (unique ID)."""

    guild: Optional[GuildModel]
    """Guild the invite is for."""

    channel: ChannelModel
    """Channel this invite is for."""

    inviter: Optional[UserModel]
    """User who created invite."""

    approximate_member_count: Optional[int]
    """Approximate count of total members."""

    expires_at: str
    """ISO8601 timestamp for expiration date."""

    roles: Optional[list[RoleModel]]
    """Roles assigned to the user upon accepting the invite."""

@dataclass
class InviteWithMetadataModel(InviteModel):
    """Represents the invite model with extra information."""

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

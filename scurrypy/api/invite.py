from dataclasses import dataclass

from ..core.model import DataModel
from ..core.snowflake import Snowflake

from ..enums.invite import InviteType

from .guilds.guild import GuildModel
from .guilds.role import GuildRoleModel
from .channels.channel import ChannelModel

from .user import UserModel

@dataclass
class InviteModel(DataModel):
    """Represents a code that adds a user to guild or group DM channel."""

    type: InviteType
    """Type of invite."""

    code: str
    """Invite code (unique ID)."""

    guild: GuildModel | None
    """Guild the invite is for."""

    channel: ChannelModel
    """Channel this invite is for."""

    inviter: UserModel | None
    """User who created invite."""

    approximate_member_count: int | None
    """Approximate count of total members."""

    expires_at: str
    """ISO8601 timestamp for expiration date."""

    roles: list[GuildRoleModel] | None
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

@dataclass
class InvitePart(DataModel):
    """Represents fields for creating an invite."""

    max_age: int | None = None
    """Duration of invite (in seconds) before it expires. 
    `0` for never or up to `604800` (max 7 days).
    Discord defaults to `86400` (24 hours).
    """

    max_uses: int | None = None
    """Max number of uses for this invite.
    `0` for unlimited or up to `100`.
    Discord defaults to `0`.
    """

    temporary: bool | None = None
    """Whether this invite grants temporary membership.
    Discord defaults to `False`.
    """

    unique: bool | None = None
    """Whether to reuse similar invite codes.
    Discord defaults to `False`.
    """

    role_ids: list[Snowflake] | None = None
    """Role IDs to be given when the user accept this invite.
    
    !!! important "Permissions"
        Requires `MANAGE_ROLES` and cannot assign roles with higher
        permissions than the sender.
    """

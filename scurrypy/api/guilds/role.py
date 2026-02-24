from dataclasses import dataclass

from ...core.model import DataModel
from ...core.snowflake import Snowflake

from ...enums.permissions import Permissions
from ..image_data import ImageDataPart

@dataclass
class GuildRoleColorModel(DataModel):
    """Represents role color data."""

    primary_color: int
    """Primary color of the role."""

    secondary_color: int
    """Secondary color of the role. Creates a gradient."""

    tertiary_color: int
    """Tertiary color of the role. Creates a holographic style."""

@dataclass
class GuildRoleModel(DataModel):
    """Represents a Discord role."""

    id: Snowflake
    """ID of the role."""

    name: str
    """Name of the role."""

    colors: GuildRoleColorModel
    """Colors of the role."""

    hoist: bool
    """If the role is pinned in user listing."""

    position: int
    """Position of the role."""

    permissions: Permissions
    """Permission bit set. [INT_LIMIT]"""

    managed: bool
    """If the role is managed by an integration."""

    mentionable: bool
    """If the role is mentionable."""

    flags: int
    """Role flags combined as a bitfield."""

    icon: str | None
    """Icon hash of the role."""

    unicode_emoji: str | None
    """Unicode emoji of the role."""

@dataclass
class GuildRoleColorsPart(DataModel):
    """Parameters for setting role colors."""

    primary_color: int | None = None
    """Primary color of the role."""

    secondary_color: int | None = None
    """Secondary color of the role. Creates a gradient."""

    tertiary_color: int | None = None
    """Tertiary color of the role. Creates a holographic style."""

@dataclass
class GuildRolePart(DataModel):
    """Parameters for creating a role."""

    name: str | None = None
    """Name of the role. Discord defaults to \"user role\"."""

    colors: GuildRoleColorsPart | None = None
    """Colors of the role. Discord defaults to primary color set to `0`."""

    icon: ImageDataPart | None = None
    """Icon of the role (if guild has `ROLE_ICONS` feature)."""

    permissions: Permissions | None = None
    """Permission bit set. [`INT_LIMIT`]"""

    hoist: bool | None = None
    """If the role is pinned in the user listing. Discord defaults to `False`."""

    mentionable: bool | None = None
    """If the role is mentionable. Discord defaults to `False`."""

    unicode_emoji: str | None = None
    """Unicode emoji of the role."""

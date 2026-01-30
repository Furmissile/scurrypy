from dataclasses import dataclass
from ..core.model import DataModel

from typing import Optional

from ..parts.image_data import ImageDataPart

@dataclass
class GuildRoleColorsPart(DataModel):
    """Parameters for setting role colors."""

    primary_color: int = None
    """Primary color of the role."""

    secondary_color: int = None
    """Secondary color of the role. Creates a gradient."""

    tertiary_color: int = None
    """Tertiary color of the role. Creates a holographic style."""

@dataclass
class GuildRolePart(DataModel):
    """Parameters for creating a role."""

    name: str = None
    """Name of the role."""

    colors: GuildRoleColorsPart = None
    """Colors of the role."""

    icon: Optional[ImageDataPart] = None
    """Icon of the role (if guild has `ROLE_ICONS` feature)."""

    permissions: int = None
    """Permission bit set. [`INT_LIMIT`]"""

    hoist: bool = None
    """If the role is pinned in the user listing."""

    mentionable: bool = None
    """If the role is mentionable."""

    unicode_emoji: Optional[str] = None
    """Unicode emoji of the role."""

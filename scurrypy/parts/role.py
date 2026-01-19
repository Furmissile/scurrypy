from dataclasses import dataclass
from ..core.model import DataModel

from typing import Optional

from .image_data import ImageData

@dataclass
class RoleColors(DataModel):
    """Parameters for setting role colors."""

    primary_color: int = None
    """Primary color of the role."""

    secondary_color: int = None
    """Secondary color of the role. Creates a gradient."""

    tertiary_color: int = None
    """Tertiary color of the role. Creates a holographic style."""

@dataclass
class CreateGuildRole(DataModel):
    """Parameters for creating a role."""

    colors: RoleColors = None
    """Colors of the role."""

    name: str = None
    """Name of the role."""

    permissions: int = 0
    """Permission bit set."""

    hoist: bool = None
    """If the role is pinned in the user listing."""

    mentionable: bool = None
    """If the role is mentionable."""

    unicode_emoji: Optional[str] = None
    """Unicode emoji of the role."""

@dataclass
class EditGuildRole(DataModel):
    """Parameters for editing a role."""

    name: Optional[str] = None
    """Name of the role."""

    permissions: Optional[int] = 0
    """Permission bit set."""

    colors: Optional[RoleColors] = None
    """Colors of the role."""

    hoist: Optional[bool] = None
    """If the role is pinned in the user listing."""

    icon: Optional[ImageData] = None
    """Role's icon image (if guild has `ROLE_ICONS` feature)."""

    unicode_emoji: Optional[str] = None
    """Unicode emoji of the role."""

    mentionable: bool = None
    """If the role is mentionable."""
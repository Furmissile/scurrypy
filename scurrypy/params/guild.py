from typing import TypedDict, Optional

from ..parts.role import RoleColorsPart
from ..parts.image_data import ImageData

class EditGuildRoleParams(TypedDict, total=False):
    """Represents fields for editing a guild role."""

    name: Optional[str]
    """Name of the role."""

    colors: Optional[RoleColorsPart]
    """Colors of the role."""

    hoist: Optional[bool]
    """Whether the role is displayed separately on the sidebar."""

    icon: Optional[ImageData]
    """Icon of the role (if guild has `ROLE_ICONS` feature)."""

    permissions: int = None
    """Permission bit set. [`INT_LIMIT`]"""

    unicode_emoji: Optional[str]
    """Unicode emoji of the role (if guilde has `ROLE_ICONS` feature)."""

    mentionable: Optional[bool]
    """Whether the role should be mentionable."""

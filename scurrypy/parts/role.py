from dataclasses import dataclass
from typing import Optional
from ..core.model import DataModel

from ..models import RoleColors

@dataclass
class Role(DataModel):
    """Parameters for creating/editing a role."""

    colors: RoleColors
    """Colors of the role."""

    name: str = None
    """Name of the role."""

    permissions: int = 0
    """Permission bit set."""

    hoist: bool = False
    """If the role is pinned in the user listing."""

    mentionable: bool = False
    """If the role is mentionable."""

    unicode_emoji: Optional[str] = None
    """Unicode emoji of the role."""

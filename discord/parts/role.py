from dataclasses import dataclass
from typing import Optional
from discord.model import DataModel

from ..models.role import RoleColors

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

    def set_color(self, hex: str):
        """Set this role's color with a hex. (format: #FFFFFF)

        Args:
            hex (str): color as a hex code

        Returns:
            (Role): self
        """
        self.color=int(hex.strip('#'), 16)
        return self

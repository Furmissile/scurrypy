from dataclasses import dataclass, field
from ..core.model import DataModel

from typing import Optional

from .image_data import ImageData

@dataclass
class CreateGuildEmoji(DataModel):
    """Represents fields for creating a guild emoji."""
    
    name: str = None
    """Name of the emoji."""
    
    image: ImageData = None
    """Image data for the icon of the emoji."""
    
    roles: list[int] = field(default_factory=list)
    """Roles able to use the emoji."""

@dataclass
class EditGuildEmoji(DataModel):
    """Represents fields for editing a guild emoji."""

    name: Optional[str] = None
    """Name of the emoji."""

    roles: Optional[list[int]] = field(default_factory=list)
    """Roles able to use the emoji."""

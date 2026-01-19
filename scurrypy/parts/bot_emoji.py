from dataclasses import dataclass
from ..core.model import DataModel

from .image_data import ImageData

@dataclass
class CreateBotEmoji(DataModel):
    """Represents fields for creating a bot emoji."""
    
    name: str = None
    """Name of the emoji."""
    
    image: ImageData = None
    """Image data for the icon of the emoji."""

@dataclass
class EditBotEmoji(DataModel):
    """Represents fields for editing a bot's emoji."""

    name: str = None
    """Name of the emoji."""
    
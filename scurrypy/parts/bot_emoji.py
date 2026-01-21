from dataclasses import dataclass
from ..core.model import DataModel

from .image_data import ImageData

@dataclass
class BotEmojiPart(DataModel):
    """Represents fields for creating a bot emoji."""
    
    name: str = None
    """Name of the emoji."""
    
    image: ImageData = None
    """Image data for the icon of the emoji."""

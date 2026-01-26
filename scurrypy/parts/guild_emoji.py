from dataclasses import dataclass, field
from ..core.model import DataModel

from .image_data import ImageDataPart

@dataclass
class GuildEmojiPart(DataModel):
    """Represents fields for creating a guild emoji."""
    
    name: str = None
    """Name of the emoji."""
    
    image: ImageDataPart = None
    """Image data for the icon of the emoji."""
    
    roles: list[int] = field(default_factory=list)
    """Roles able to use the emoji."""

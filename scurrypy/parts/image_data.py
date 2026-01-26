from dataclasses import dataclass, field
from ..core.model import DataModel

@dataclass
class ImageDataPart(DataModel):
    """Represents Discord's data URI scheme for images."""
    
    path: str = None
    """Path to image."""

    def to_dict(self):
        import base64, mimetypes

        mime, _ = mimetypes.guess_type(self.path)
        if mime is None:
            raise ValueError("Unknown file type.")

        with open(self.path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        return f"data:{mime};base64,{encoded}"

@dataclass
class ImageAssetPart(DataModel):
    """Represents fields for creating an image asset."""

    filename: str = None
    """Name of the file."""

    content_type: str = field(init=False)
    """Content type (internally set)."""

    data: bytes = field(init=False)
    """Binary data (internally set)."""

    def to_dict(self):
        import mimetypes

        mime, _ = mimetypes.guess_type(self.filename)
        if mime is None:
            raise ValueError("Unknown file type.")
        
        with open(self.filename, 'rb') as f:
            self.data = f.read()

        return {
            'filename': self.filename,
            'content_type': mime,
            "value": self.data
        }

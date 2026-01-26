from dataclasses import dataclass, field
from ..core.model import DataModel

@dataclass
class AttachmentPart(DataModel):
    """Represents an attachment."""

    path: str = None
    """Relative path to the file."""

    description: str = None
    """Description of the file."""

    id: int = field(init=False, default=None)
    """ID of the attachment (internally set)."""

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.path.split('/')[-1],
            'description': self.description
        }

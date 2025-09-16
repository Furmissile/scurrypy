from dataclasses import dataclass

from ..model import DataModel

@dataclass
class _Attachment(DataModel):
    """Represents an attachment."""
    id: int
    path: str
    filename: str
    description: str

    def _to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'description': self.description
        }

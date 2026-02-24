from dataclasses import dataclass, field

from ...core.model import DataModel
from ...core.snowflake import Snowflake
from ...core.exceptions import MissingField
from ...core.types import Serialized

@dataclass
class AttachmentModel(DataModel):
    """Represents an attachment object."""

    id: Snowflake
    """Attachment ID."""

    filename: str
    """Name of the file."""

    title: str | None
    """Title of the file."""

    description: str | None
    """Description of the file."""

    content_type: str | None
    """Media type of the file."""

    size: int
    """Size of file (in bytes)."""

    url: str
    """Source URL of the file."""

    proxy_url: str
    """A proxied URL of the file."""

    height: int | None
    """Height of file (if image)."""

    width: int | None
    """Width of file (if image)."""

    ephemeral: bool | None
    """Whether this file is ephemeral."""

    flags: int | None
    """Attachment flags as a combined bitfield."""

@dataclass
class AttachmentPart(DataModel):
    """Represents an attachment."""

    path: str | None = None
    """Relative path to the file."""

    description: str | None = None
    """Description of the file."""

    id: int | None = field(init=False, default=None)
    """ID of the attachment (internally set)."""

    def to_dict(self) -> Serialized:
        """Serialize this attachment.

        Raises:
            (MissingField): _description_

        Returns:
            (Serialized): serialized attachment
        """
        if self.path is None:
            raise MissingField("AttachmentPart.path must be set before serialization")
        
        return {
            'id': self.id,
            'filename': self.path.split('/')[-1],
            'description': self.description
        }

from ..core.model import DataModel
from ..core.types import JSON

from ..enums.events import EventType

from typing import ClassVar

class Event(DataModel):
    """Marker class for all gateway events."""

    dispatch_name: ClassVar[EventType]
    """Dispatch name of event."""

    raw: JSON
    """Event's raw JSON payload."""

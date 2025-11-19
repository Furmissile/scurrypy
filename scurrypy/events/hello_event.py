from dataclasses import dataclass
from ..core.model import DataModel

@dataclass
class HelloEvent(DataModel):
    """Heartbeat interval event."""

    heartbeat_interval: int
    """Heartbeat interval in milliseconds."""

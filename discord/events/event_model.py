from dataclasses import dataclass
from ..model import DataModel
from ..config import BaseConfig

@dataclass
class EventModel(DataModel):
    """Event Model for event-driven fields common among all events."""

    config: BaseConfig
    """User-defined bot config for persistent data."""

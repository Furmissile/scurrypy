from dataclasses import dataclass
from typing import Optional
from ..model import DataModel
from .application import ApplicationModel

@dataclass
class IntegrationModel(DataModel):
    """Represents a guild integration."""

    id: int
    """ID of the integration."""

    name: str
    """Name of the integration."""

    type: str
    """Type of integration (e.g., twitch, youtube, discord, or guild_subscription)."""

    enabled: bool
    """If the integration is enabled."""

    application: Optional[ApplicationModel] = None
    """The bot aaplication for Discord integrations."""

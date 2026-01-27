from dataclasses import dataclass
from ..core.model import DataModel
from typing import Optional
from .base_event import Event

from ..models.integration import IntegrationModel

@dataclass
class GuildIntegrationCreateEvent(Event, IntegrationModel):
    """Received when an integration is created."""

    guild_id: int
    """Guild ID of the created integration."""

@dataclass
class GuildIntegrationUpdateEvent(Event, IntegrationModel):
    """Received when an integration is created."""

    guild_id: int
    """Guild ID of the updated integration."""

@dataclass
class GuildIntegrationsUpdateEvent(Event, DataModel):
    """Received when a guild's integration is updated."""

    guild_id: int
    """ID of the guild whose integrations were updated."""

@dataclass
class GuildIntegrationDeleteEvent(Event, DataModel):
    """Received when a guild's integration is deleted."""

    id: int
    """ID of the deleted integration."""

    guild_id: int
    """Guild ID of the deleted integration."""

    application_id: Optional[int]
    """ID of the bot for this Discord integration."""

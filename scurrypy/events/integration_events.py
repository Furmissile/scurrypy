from dataclasses import dataclass

from ..core.model import DataModel
from ..core.snowflake import Snowflake

from .base_event import Event

from ..enums.events import EventType

from ..api.integration import IntegrationModel

@dataclass
class GuildIntegrationCreateEvent(Event, IntegrationModel):
    """Received when an integration is created."""

    dispatch_name = EventType.INTEGRATION_CREATE

    guild_id: Snowflake
    """Guild ID of the created integration."""

@dataclass
class GuildIntegrationUpdateEvent(Event, IntegrationModel):
    """Received when an integration is created."""

    dispatch_name = EventType.INTEGRATION_UPDATE

    guild_id: Snowflake
    """Guild ID of the updated integration."""

@dataclass
class GuildIntegrationsUpdateEvent(Event, DataModel):
    """Received when a guild's integration is updated."""

    dispatch_name = EventType.GUILD_INTEGRATIONS_UPDATE

    guild_id: Snowflake
    """ID of the guild whose integrations were updated."""

@dataclass
class GuildIntegrationDeleteEvent(Event, DataModel):
    """Received when a guild's integration is deleted."""

    dispatch_name = EventType.INTEGRATION_DELETE

    id: Snowflake
    """ID of the deleted integration."""

    guild_id: Snowflake
    """Guild ID of the deleted integration."""

    application_id: Snowflake | None
    """ID of the bot for this Discord integration."""

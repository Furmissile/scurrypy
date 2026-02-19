from dataclasses import dataclass

from ..core.model import DataModel
from ..core.snowflake import Snowflake

from ..enums.integration import IntegrationType

from .application import ApplicationModel

@dataclass
class IntegrationModel(DataModel):
    """Represents a guild integration."""

    id: Snowflake
    """ID of the integration."""

    name: str
    """Name of the integration."""

    type: IntegrationType
    """Type of integration."""

    enabled: bool
    """If the integration is enabled."""

    application: ApplicationModel | None
    """The bot application for Discord integrations."""

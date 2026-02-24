from dataclasses import dataclass

from ..core.model import DataModel
from ..core.snowflake import Snowflake

from .base_event import Event

from ..enums.events import EventType

from ..api.guilds.role import GuildRoleModel

@dataclass
class RoleCreateEvent(Event, DataModel):
    """Received when a guild role is created."""

    dispatch_name = EventType.ROLE_CREATE

    guild_id: Snowflake
    """Guild ID of the role."""

    role: GuildRoleModel
    """The new role."""

@dataclass
class RoleUpdateEvent(Event, DataModel):
    """Received when a guild role is updated."""

    dispatch_name = EventType.ROLE_UPDATE

    guild_id: Snowflake
    """Guild ID of the role."""

    role: GuildRoleModel
    """The new role."""

@dataclass
class RoleDeleteEvent(Event, DataModel):
    """Received when a guild role is deleted."""

    dispatch_name = EventType.ROLE_DELETE

    guild_id: Snowflake
    """Guild ID of the role."""

    role_id: Snowflake
    """Role ID of the role."""

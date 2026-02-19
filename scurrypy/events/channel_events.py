from dataclasses import dataclass

from ..core.model import DataModel
from ..core.snowflake import Snowflake

from .base_event import Event

from ..api.channels.channel import ChannelModel

@dataclass
class ChannelCreateEvent(Event, ChannelModel):
    """Received when a guild channel has been created."""
    pass

@dataclass
class ChannelUpdateEvent(Event, ChannelModel):
    """Received when a guild channel has been updated.

    !!! note
        Not send when `last_message_id` is changed.
    """
    pass

@dataclass
class ChannelDeleteEvent(Event, ChannelModel):
    """Received when a guild channel has been deleted."""
    pass

@dataclass
class ChannelPinsUpdateEvent(Event, DataModel):
    """Pin update event."""
    
    channel_id: Snowflake
    """ID of channel where the pins were updated."""

    guild_id: Snowflake | None
    """ID of the guild where the pins were updated."""

    last_pin_timestamp: str | None
    """ISO8601 formatted timestamp of the last pinned message in the channel."""

@dataclass
class WebhooksUpdateEvent(Event, DataModel):
    """Received when a guild's channel webhook is created, updated, or deleted."""

    guild_id: Snowflake
    """ID of the guild."""

    channel_id: Snowflake
    """ID of the channel."""

from dataclasses import dataclass
from ..core.model import DataModel
from .base_event import Event

from typing import Optional

from ..models.channel import ChannelModel

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
    
    channel_id: int
    """ID of channel where the pins were updated."""

    guild_id: Optional[int]
    """ID of the guild where the pins were updated."""

    last_pin_timestamp: Optional[str]
    """ISO8601 formatted timestamp of the last pinned message in the channel."""

@dataclass
class WebhooksUpdateEvent(Event, DataModel):
    """Received when a guild's channel webhook is created, updated, or deleted."""

    guild_id: int
    """ID of the guild."""

    channel_id: int
    """ID of the channel."""

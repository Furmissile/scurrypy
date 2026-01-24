from dataclasses import dataclass
from ..core.model import DataModel
from .base_event import Event

from typing import Optional

from ..models.channel import ChannelModel, ThreadMemberModel

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
class ChannelPinsUpdateEvent(Event, DataModel):
    """Pin update event."""
    
    channel_id: int
    """ID of channel where the pins were updated."""

    guild_id: Optional[int]
    """ID of the guild where the pins were updated."""

    last_pin_timestamp: Optional[str]
    """ISO8601 formatted timestamp of the last pinned message in the channel."""

@dataclass
class ChannelDeleteEvent(Event, ChannelModel):
    """Received when a guild channel has been deleted."""
    pass

@dataclass
class ThreadCreateEvent(Event, ChannelModel):
    """Received when a thread is created."""

    newly_created: bool
    """Whether the thread has just been created."""

@dataclass
class ThreadUpdateEvent(Event, ChannelModel):
    """Received when a thread is updated.
    
    !!! note
        Not send when `last_message_id` is changed.
    """
    pass

@dataclass
class ThreadMembersUpdateEvent(Event, DataModel):
    """Received when someone is added or removed from a thread.
    
    !!! important
        Without the `GUILD_MEMBERS` privileged intent, this event only fires if the 
        bot was added or removed from a thread.
    """

    id: int
    """ID of the thread."""

    guild_id: int
    """ID of the guild."""

    member_count: int
    """Approximate number of members in the thread (max `50`)."""

    added_members: Optional[list[ThreadMemberModel]]
    """Users who were added to the thread"""

    removed_member_ids: Optional[list[int]]
    """ID of the users who were removed from the thread."""

@dataclass
class ThreadDeleteEvent(Event, DataModel):
    """Received when a thread is deleted."""

    id: int
    """ID of the thread."""
    
    guild_id: Optional[int]
    """Guild ID of the thread."""
    
    parent_id: int
    """ID of the parent channel."""
    
    type: int
    """Type of thread."""

@dataclass
class BulkMessageDeleteEvent(Event, DataModel):
    """Received when bulk deleting messages."""

    ids: list[int]
    """IDs of the messages that were deleted."""

    channel_id: int
    """ID of the channel."""

    guild_id: Optional[int]
    """ID of the guild."""

@dataclass
class WebhooksUpdateEvent(Event, DataModel):
    """Received when a guild's channel webhook is created, updated, or deleted."""

    guild_id: int
    """ID of the guild."""

    channel_id: int
    """ID of the channel."""
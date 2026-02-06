from dataclasses import dataclass
from ..core.model import DataModel
from ..core.snowflake import Snowflake
from .base_event import Event

from typing import Optional

from ..models.channel import ChannelModel, ThreadMemberModel

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
class ThreadDeleteEvent(Event, DataModel):
    """Received when a thread is deleted."""

    id: Snowflake
    """ID of the thread."""
    
    guild_id: Optional[Snowflake]
    """Guild ID of the thread."""
    
    parent_id: Snowflake
    """ID of the parent channel."""
    
    type: int
    """Type of thread."""

@dataclass
class ThreadMemberUpdateEvent(Event, ThreadMemberModel):
    """Received when a thread member for the bot is updated."""

    guild_id: Snowflake
    """ID of the guild."""

@dataclass
class ThreadMembersUpdateEvent(Event, DataModel):
    """Received when someone is added or removed from a thread.
    
    !!! important
        Without the `GUILD_MEMBERS` privileged intent, this event only fires if the 
        bot was added or removed from a thread.
    """

    id: Snowflake
    """ID of the thread."""

    guild_id: Snowflake
    """ID of the guild."""

    member_count: int
    """Approximate number of members in the thread (max `50`)."""

    added_members: Optional[list[ThreadMemberModel]]
    """Users who were added to the thread"""

    removed_member_ids: Optional[list[Snowflake]]
    """ID of the users who were removed from the thread."""

@dataclass
class ThreadListSyncEvent(Event, DataModel):
    """Received when the bot gains access to a channel."""

    guild_id: Snowflake
    """ID of the guild."""

    channel_ids: Optional[list[Snowflake]]
    """Parent channel IDs of the threads being synced."""

    threads: list[ChannelModel]
    """Active threads in the given channel that the bot can access."""

    members: list[ThreadMemberModel]
    """Thread members from the synced threads that the bot an access."""

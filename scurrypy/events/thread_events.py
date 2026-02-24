from dataclasses import dataclass

from ..core.model import DataModel
from ..core.snowflake import Snowflake

from .base_event import Event

from ..enums.channel import ChannelType
from ..enums.events import EventType

from ..api.channels.channel import ChannelModel
from ..api.channels.threads import ThreadMemberModel

@dataclass
class ThreadCreateEvent(Event, ChannelModel):
    """Received when a thread is created."""

    dispatch_name = EventType.THREAD_CREATE

    newly_created: bool
    """Whether the thread has just been created."""

@dataclass
class ThreadUpdateEvent(Event, ChannelModel):
    """Received when a thread is updated.
    
    !!! note
        Not send when `last_message_id` is changed.
    """

    dispatch_name = EventType.THREAD_UPDATE

@dataclass
class ThreadDeleteEvent(Event, DataModel):
    """Received when a thread is deleted."""

    dispatch_name = EventType.THREAD_DELETE

    id: Snowflake
    """ID of the thread."""
    
    guild_id: Snowflake | None
    """Guild ID of the thread."""
    
    parent_id: Snowflake
    """ID of the parent channel."""
    
    type: ChannelType
    """Type of thread."""

@dataclass
class ThreadMemberUpdateEvent(Event, ThreadMemberModel):
    """Received when a thread member for the bot is updated."""

    dispatch_name = EventType.THREAD_MEMBER_UPDATE

    guild_id: Snowflake
    """ID of the guild."""

@dataclass
class ThreadMembersUpdateEvent(Event, DataModel):
    """Received when someone is added or removed from a thread.
    
    !!! important
        Without the `GUILD_MEMBERS` privileged intent, this event only fires if the 
        bot was added or removed from a thread.
    """

    dispatch_name = EventType.THREAD_MEMBERS_UPDATE

    id: Snowflake
    """ID of the thread."""

    guild_id: Snowflake
    """ID of the guild."""

    member_count: int
    """Approximate number of members in the thread (max `50`)."""

    added_members: list[ThreadMemberModel] | None
    """Users who were added to the thread"""

    removed_member_ids: list[Snowflake] | None
    """ID of the users who were removed from the thread."""

@dataclass
class ThreadListSyncEvent(Event, DataModel):
    """Received when the bot gains access to a channel."""

    dispatch_name = EventType.THREAD_LIST_SYNC

    guild_id: Snowflake
    """ID of the guild."""

    channel_ids: list[Snowflake] | None
    """Parent channel IDs of the threads being synced."""

    threads: list[ChannelModel]
    """Active threads in the given channel that the bot can access."""

    members: list[ThreadMemberModel]
    """Thread members from the synced threads that the bot an access."""

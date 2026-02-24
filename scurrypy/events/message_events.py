from dataclasses import dataclass

from ..core.model import DataModel
from ..core.snowflake import Snowflake

from .base_event import Event

from ..enums.events import EventType

from ..api.messages.message import MessageModel

from ..api.user import GuildMemberModel

@dataclass
class MessageCreateEvent(Event, MessageModel):
    """Received when a message is created.
    
    !!! note
        `member` may be missing on `MESSAGE_CREATE` and `MESSAGE_UPDATE`. Use `author` when you need the user.
    """

    dispatch_name = EventType.MESSAGE_CREATE

    guild_id: Snowflake | None
    """Guild ID of the updated message (if in a guild channel)."""

    member: GuildMemberModel | None
    """Partial Member object of the author of the message."""

@dataclass
class MessageUpdateEvent(Event, MessageModel):
    """Received when a message is updated."""

    dispatch_name = EventType.MESSAGE_UPDATE

    guild_id: Snowflake | None
    """Guild ID of the updated message (if in a guild channel)."""

    member: GuildMemberModel | None
    """Partial Member object of the author of the message."""

@dataclass
class MessageDeleteEvent(Event, DataModel):
    """Received when a message is deleted."""

    dispatch_name = EventType.MESSAGE_DELETE

    id: Snowflake
    """ID of the deleted message."""

    channel_id: Snowflake
    """Channel ID of the deleted message."""

    guild_id: Snowflake | None
    """Guild ID of the deleted message (if in a guild channel)."""

@dataclass
class BulkMessageDeleteEvent(Event, DataModel):
    """Received when bulk deleting messages."""

    dispatch_name = EventType.BULK_MESSAGE_DELETE

    ids: list[Snowflake]
    """IDs of the messages that were deleted."""

    channel_id: Snowflake
    """ID of the channel."""

    guild_id: Snowflake | None
    """ID of the guild."""

from dataclasses import dataclass
from typing import Optional
from ..model import DataModel

from ..resources.message import Message
from ..models.member import MemberModel

@dataclass
class MessageCreateEvent(DataModel):
    """Received when a message is created."""
    message: Message
    """Message resource object. See [`Resource.Message`][scurrypy.resources.message.Message]."""

    guild_id: Optional[int]
    """Guild ID of the updated message (if in a guild channel)."""

    member: Optional[MemberModel]  # guild-only author info
    """Partial Member object of the author of the message. See [`MemberModel`][scurrypy.models.member.MemberModel]."""
    
@dataclass
class MessageUpdateEvent(DataModel):
    """Received when a message is updated."""
    message: Message
    """Message resource object. See [`Resource.Message`][scurrypy.resources.message.Message]."""

    guild_id: Optional[int]
    """Guild ID of the updated message (if in a guild channel)."""

    member: Optional[MemberModel]
    """Partial Member object of the author of the message. See [`MemberModel`][scurrypy.models.member.MemberModel]."""

@dataclass
class MessageDeleteEvent(DataModel):
    """Received when a message is deleted."""

    id: int
    """ID of the deleted message."""

    channel_id: int
    """Channel ID of the deleted message."""

    guild_id: Optional[int]
    """Guild ID of the deleted message (if in a guild channel)."""

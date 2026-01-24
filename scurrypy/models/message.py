from dataclasses import dataclass
from ..core.model import DataModel

from typing import Optional

from .user import UserModel

@dataclass
class MessageModel(DataModel):
    """Represents a Discord message."""

    id: int
    """ID of the message."""

    channel_id: int
    """Channel ID of the message."""

    author: UserModel
    """User data of author of the message."""
    
    content: str
    """Content of the message."""

    pinned: bool
    """If the message is pinned."""

    type: int
    """Type of message."""

    webhook_id: Optional[int]
    """ID of the webhook if the message is a webhook."""

    timestamp: Optional[str]
    """Timestamp of when the message was sent."""

@dataclass
class PinnedMessageModel(DataModel):
    """Represents a pinned message."""

    message: MessageModel
    """Message resource of the pinned message."""

    pinned_at: Optional[str]
    """ISO8601 timestamp of when the message was pinned."""

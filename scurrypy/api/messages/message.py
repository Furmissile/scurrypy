from dataclasses import dataclass

from ...bases.components import Component

from ...core.model import DataModel
from ...core.snowflake import Snowflake
from ...core.types import Serialized

from ...enums.message import MessageType, MessageFlags, MessageReferenceType

from ..components.layout import Container, ActionRow
from ..messages.attachment import AttachmentModel, AttachmentPart
from ..messages.embed import Embed
from ..messages.reaction import ReactionModel
from ..channels.channel import ChannelModel
from ..guilds.role import GuildRoleModel

from ..user import UserModel

from typing import Self

@dataclass
class MessageModel(DataModel):
    """Represents a Discord message."""

    id: Snowflake
    """ID of the message."""

    channel_id: Snowflake
    """Channel ID of the message."""

    author: UserModel
    """User data of author of the message."""
    
    content: str
    """Content of the message."""

    pinned: bool
    """If the message is pinned."""

    type: MessageType
    """Type of message."""

    flags: MessageFlags
    """Message flags."""

    attachments: list[AttachmentModel]
    """Attached files."""

    embeds: list[Embed]
    """Embedded content."""

    thread: ChannelModel | None
    """Thread created from the message."""

    reactions: list[ReactionModel]
    """Reactions to the message."""

    webhook_id: Snowflake | None
    """ID of the webhook if the message is a webhook."""

    timestamp: str | None
    """Timestamp of when the message was sent."""

    edited_timestamp: str | None
    """Timestamp of when the message was last edited."""

    mention_everyone: bool
    """Whether the message mentions everyone."""

    mentions: list[UserModel]
    """List of mentioned users in the message."""

    mention_roles: list[GuildRoleModel]
    """List of mentioned roles in the message."""

    components: list[Component]
    """Components contained in the message."""

@dataclass
class PinnedMessageModel(DataModel):
    """Represents a pinned message."""

    message: MessageModel
    """Message resource of the pinned message."""

    pinned_at: str | None
    """ISO8601 timestamp of when the message was pinned."""

@dataclass
class MessageReferencePart(DataModel):
    """Represents the Message Reference object."""

    message_id: Snowflake | None = None
    """ID of the originating message."""

    channel_id: Snowflake | None = None
    """
        Channel ID of the originating message.
        !!! note
            Optional for default type, but REQUIRED for forwards.
    """

    type: MessageReferenceType | None = None
    """Type of reference. Discord defaults to `MessageReferenceTypes.DEFAULT`."""

@dataclass
class MessagePart(DataModel):
    """Represents a Discord Message."""

    content: str | None = None
    """Message text content."""

    flags: MessageFlags | None = None
    """Message flags. Discord defaults to `MessageFlags.NO_FLAGS`."""

    components: list[ActionRow | Container] | None = None
    """Components to be attached to this message."""

    attachments: list[AttachmentPart] | None = None
    """Attachments to be attached to this message."""

    embeds: list[Embed] | None = None
    """Embeds to be attached to this message."""

    message_reference: MessageReferencePart | None = None
    """Message reference if reply."""

    def _prepare(self) -> Self:
        """Prepares MessagePart for ANY internally set attributes.

        Returns:
            (MessagePart): self
        """
        # set attachment IDs (if any)
        if self.attachments:
            for idx, file in enumerate(self.attachments):
                file.id = idx
        else:
            self.attachments = []
        
        return self

    def to_dict(self) -> Serialized:
        if self.components:
            for component in self.components:
                if not isinstance(component, Container):
                    continue

                if not self.flags or MessageFlags.IS_COMPONENTS_V2 not in self.flags:
                    raise ValueError("V2 components are used but MessageFlags.IS_COMPONENTS_V2 is not set.")
        
        return super().to_dict()

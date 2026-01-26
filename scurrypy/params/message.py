from typing import TypedDict

from ..parts.embed import EmbedPart
from ..parts.components import ActionRowPart
from ..parts.components_v2 import ContainerPart
from ..parts.attachment import AttachmentPart
from ..parts.message import MessageReferencePart

class EditMessageParams(TypedDict, total=False):
    """Parameters for editing a message"""

    content: str
    """Message text content."""

    flags: int
    """Message flags. See [`MessageFlags`][scurrypy.parts.message.MessageFlags].
    
    !!! note
        Can only set `SUPPRESS_EMBEDS` and `IS_COMPONENTS_V2`
    """

    components: list[ActionRowPart | ContainerPart]
    """Components to be attached to this message."""

    attachments: list[AttachmentPart]
    """Attachments to be attached to this message."""

    embeds: list[EmbedPart]
    """Embeds to be attached to this message."""

    message_reference: MessageReferencePart
    """Message reference if reply."""

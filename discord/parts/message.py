from dataclasses import dataclass, field
from typing import Optional, TypedDict, Unpack, Literal
from discord.model import DataModel
from .embed import EmbedBuilder
from .action_row import ActionRow
from .components_v2 import Container
from .attachment import _Attachment

class MessageFlags:
    """Flags that can be applied to a message."""
    CROSSPOSTED = 1 << 0
    """Message has been published."""

    IS_CROSSPOST = 1 << 1
    """Message originated from another channel."""

    SUPPRESS_EMBEDS = 1 << 2
    """Hide embeds (if any)."""

    EPHEMERAL = 1 << 6
    """Only visible to the invoking user."""

    LOADING = 1 << 7
    """Thinking response."""

    IS_COMPONENTS_V2 = 1 << 15
    """This message includes Discord's V2 Components."""

class MessageFlagParams(TypedDict, total=False):
    """Parameters for setting message flags."""
    crossposted: bool
    is_crosspost: bool
    suppress_embeds: bool
    ephemeral: bool
    loading: bool
    is_components_v2: bool

@dataclass
class _MessageReference(DataModel):
    message_id: int
    channel_id: int
    type: int = 0

@dataclass
class MessageBuilder(DataModel):
    """Describes expected params when editing/creating a message."""

    content: Optional[str] = None
    """Message text content."""

    flags: Optional[int] = 0
    """Message flags. See [`MessageFlags`][discord.parts.message.MessageFlags] for details."""

    components: Optional[list[ActionRow | Container]] = field(default_factory=list)
    """Components to be attached to this message."""

    attachments: Optional[list[_Attachment]] = field(default_factory=list)
    """Attachments to be attached to this message."""

    embeds: Optional[list[EmbedBuilder]] = field(default_factory=list)
    """Embeds to be attached to this message."""

    message_reference: Optional[_MessageReference] = None
    """Message reference if reply."""

    def add_row(self, row: ActionRow):
        """Add an action row to this message.

        Args:
            row (ActionRow): the ActionRow object

        Returns:
            (MessageBuilder): self
        """
        self.components.append(row)
        return self
    
    def add_container(self, container: Container, *, has_container_boarder: bool = False):
        """Add a container to this message.

        Args:
            container (Container): the Container object.
            has_container_boarder (bool, optional): If message should be contained in an Embed-like container. Defaults to False.

        Returns:
            (MessageBuilder): self
        """
        if has_container_boarder:
            self.components.append(container)
        else:
            self.components.extend(container.components)
        return self
    
    def add_embed(self, embed: EmbedBuilder):
        """Add an embed to this message.

        Args:
            embed (EmbedBuilder): The EmbedBuilder object.

        Returns:
            (MessageBuilder): self
        """
        self.embeds.append(embed)
        return self

    def add_attachment(self, file_path: str, description: str = None):
        """Add an attachment to this message

        Args:
            file_path (str): full qualifying path to file
            description (str, optional): file descriptor. Defaults to None.

        Returns:
            (MessageBuilder): self
        """
        import os
        
        self.attachments.append(
            _Attachment(
                id=len(self.attachments), 
                filename=os.path.basename(file_path), 
                path=file_path,
                description=description
            )
        )
        return self
    
    def set_flags(self, **flags: Unpack[MessageFlagParams]):
        """Set this message's flags using MessageFlagParams.

        Args:
            flags (Unpack[MessageFlagParams]): message flags to set. (set respective flag to True to toggle.)

        Raises:
            (ValueError): invalid flag

        Returns:
            (MessageBuilder): self
        """
        _flag_map = {
            'crossposted': MessageFlags.CROSSPOSTED,
            'is_crosspost': MessageFlags.IS_CROSSPOST,
            'suppress_embeds': MessageFlags.SUPPRESS_EMBEDS,
            'ephemeral': MessageFlags.EPHEMERAL,
            'loading': MessageFlags.LOADING,
            'is_components_v2': MessageFlags.IS_COMPONENTS_V2,
        }

        # each flag maps to a specific combined bit!
        for name, value in flags.items():
            if name not in _flag_map:
                raise ValueError(f"Invalid flag: {name}")
            if value:
                self.flags |= _flag_map[name]
                
        return self

    def _set_reference(self, 
        message_id: int, 
        channel_id: int,
        ref_type: Literal['Default', 'Forward'] = 'Default'
    ):
        """Internal helper for setting this message's reference message. Used in replies.

        Args:
            message_id (int): message to reference

        Returns:
            (MessageBuilder): self
        """
        _ref_types = {
            'DEFAULT': 0,
            'FORWARD': 1
        }
        self.message_reference = _MessageReference(
            type=_ref_types.get(ref_type.upper()), 
            channel_id=channel_id,
            message_id=message_id
        )
        return self

from dataclasses import dataclass, field
from typing import Literal, Optional
from ..model import DataModel

from .component_types import *

from ..models.emoji import EmojiModel

class _ButtonStyles:
    """Represents button styles for a Button component."""
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5

@dataclass
class _Button(DataModel, ActionRowChild, SectionAccessory):
    """Represents the Button component."""
    style: int
    custom_id: str
    label: Optional[str] = None
    emoji: EmojiModel = None
    url: Optional[str] = None
    disabled: Optional[bool] = False
    type: Literal[2] = field(init=False, default=2)

@dataclass
class _SelectOption(DataModel):
    """Represents the Select Option component"""
    label: str
    value: str
    description: Optional[str] = None # appears below the label
    emoji: Optional[EmojiModel] = None
    default: Optional[bool] = False

@dataclass
class StringSelect(DataModel, ActionRowChild, LabelChild):
    """Represents the String Select component."""
    custom_id: str
    options: list[_SelectOption] = field(default_factory=list)
    placeholder: Optional[str] = None
    min_values: Optional[int] = 0
    max_values: Optional[int] = 1
    required: Optional[bool] = False
    disabled: Optional[bool] = False # does not work on Modals!
    type: Literal[3] = field(init=False, default=3)

    def add_option(self,
        *,
        label: str,
        value: str,
        description: str = None,
        emoji: str | EmojiModel = None,
        default: bool = False
    ):
        """Add an option to this string select component.

        Args:
            label (str): option text
            value (str): analogous to button's custom ID
            description (str, optional): option subtext
            emoji (str | EmojiModel, optional): string if unicode emoji, EmojiModel if custom
            default (bool, optional): if this option should be the default option. Defaults to False.

        Returns:
            (StringSelect): self
        """
        if isinstance(emoji, str):
            emoji = EmojiModel(name=emoji)

        self.options.append(
            _SelectOption(
                label=label,
                value=value,
                description=description,
                emoji=emoji,
                default=default
            )
        )
        return self

@dataclass
class _DefaultValue(DataModel):
    """Represents the Default Value for Select components."""

    id: int   # ID of role, user, or channel
    type: Literal["role", "user", "channel"]

@dataclass
class UserSelect(DataModel, ActionRowChild):
    """Represents the User Select component."""
    custom_id: str
    placeholder: Optional[str] = None
    default_values: list[_DefaultValue] = field(default_factory=list)
    min_values: Optional[int] = 0
    max_values: Optional[int] = 1
    disabled: Optional[bool] = False
    type: Literal[5] = field(init=False, default=5)

    def add_default_value(self, user_id: int):
        self.default_values.append(_DefaultValue(user_id, 'user'))
        return self

@dataclass
class RoleSelect(DataModel, ActionRowChild):
    """Represents the Role Select component."""
    custom_id: str
    placeholder: Optional[str] = None
    default_values: list[_DefaultValue] = field(default_factory=list)
    min_values: Optional[int] = 0
    max_values: Optional[int] = 1
    disabled: Optional[bool] = False
    type: Literal[6] = field(init=False, default=6)

    def add_default_value(self, role_id: int):
        self.default_values.append(_DefaultValue(role_id, 'role'))
        return self

@dataclass
class MentionableSelect(DataModel, ActionRowChild):
    """Represents the Mentionable Select component."""
    custom_id: str
    placeholder: Optional[str] = None
    default_values: list[_DefaultValue] = field(default_factory=list)
    min_values: Optional[int] = 0
    max_values: Optional[int] = 1
    disabled: Optional[bool] = False
    type: Literal[7] = field(init=False, default=7)

    def add_default_value(self, role_or_user_id: int, role_or_user: Literal['user', 'role']):
        self.default_values.append(_DefaultValue(role_or_user_id, role_or_user))
        return self

@dataclass
class ChannelSelect(DataModel, ActionRowChild):
    """Represents the Channel Select component."""
    custom_id: str
    placeholder: Optional[str] = None
    default_values: list[_DefaultValue] = field(default_factory=list)
    min_values: Optional[int] = 0
    max_values: Optional[int] = 1
    disabled: Optional[bool] = False
    type: Literal[8] = field(init=False, default=8)

    def add_default_value(self, channel_id: int):
        self.default_values.append(_DefaultValue(channel_id, 'channel'))
        return self

@dataclass
class ActionRow(DataModel, ContainerChild):
    """Represents a container of interactable components."""
    type: Literal[1] = field(init=False, default=1)
    components: list[ActionRowChild] = field(default_factory=list)

    def add_button(self, 
        *,
        style: Literal['Primary', 'Secondary', 'Success', 'Danger', 'Link'],
        label: str, 
        custom_id: str,
        emoji: str | EmojiModel = None,
        disable: bool = False
    ):
        """Add a button to this action row. (5 per row)
        
        Args:
            style (Literal['Primary', 'Secondary', 'Success', 'Danger', 'Link']): 
                button style as a string
            label (str): button text
            custom_id (str): developer-defined button ID
            emoji (str | EmojiModel, Optional): str if unicode emoji, EmojiModal if custom
            disable (bool, Optional): if this button should be pressable. Defaults to False.

        Returns:
            (ActionRow): self
        """
        _styles = {
            'PRIMARY': _ButtonStyles.PRIMARY,
            'SECONDARY': _ButtonStyles.SECONDARY,
            'SUCCESS': _ButtonStyles.SUCCESS,
            'DANGER': _ButtonStyles.DANGER,
            'LINK': _ButtonStyles.LINK
        }

        if isinstance(emoji, str):
            emoji = EmojiModel(name=emoji)

        self.components.append(
            _Button(
                style=_styles.get(style.upper()),
                label=label,
                custom_id=custom_id,
                emoji=emoji,
                disabled=disable
            )
        )
        return self

    def string_select(self, select: StringSelect):
        """Add a string select to this action row. (1 per row)

        Args:
            select (StringSelect): the StringSelect option object

        Returns:
            (ActionRow): self
        """
        self.components.append(select)
        return self
    
    def user_select(self, select: UserSelect):
        """Add a user select to this action row. (1 per row)

        Args:
            select (UserSelect): the UserSelect option object

        Returns:
            (ActionRow): self
        """
        self.components.append(select)
        return self
    
    def role_select(self, select: RoleSelect):
        """Add a role select to this action row. (1 per row)

        Args:
            select (RoleSelect): the RoleSelect option object

        Returns:
            (ActionRow): self
        """
        self.components.append(select)
        return self
    
    def channel_select(self, select: ChannelSelect):
        """Add a channel select to this action row. (1 per row)

        Args:
            select (ChannelSelect): the ChannelSelect option object

        Returns:
            (ActionRow): self
        """
        self.components.append(select)
        return self
    
    def mentionable_select(self, select: MentionableSelect):
        """Add a mentionable select to this action row. (1 per row)

        Args:
            select (MentionableSelect): the MentionableSelect option object

        Returns:
            (ActionRow): self
        """
        self.components.append(select)
        return self

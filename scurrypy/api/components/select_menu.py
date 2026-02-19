from dataclasses import dataclass, field

from ...core.model import DataModel
from ...core.snowflake import Snowflake

from ...bases.components import (
    ActionRowChild, 
    LabelChild,
    Component
)

from ...enums.components import ComponentType, DefaultValueType

from ..emoji import EmojiModel

@dataclass
class SelectOption(DataModel):
    """Represents the Select Option component."""

    label: str | None = None
    """User-facing name of the option."""

    value: str | None = None
    """Developer-defined value of the option."""

    description: str | None = None
    """Additional description of the option."""

    emoji: EmojiModel | None = None
    """Partial emoji object."""

    default: bool | None = None
    """Whether this option is selected by default. Discord defaults to `False`."""

@dataclass
class StringSelect(DataModel, Component, ActionRowChild, LabelChild):
    """Represents the String Select component.
    
    A String Select allows users to select one or more provided options.
    """

    custom_id: str | None = None
    """ID for the select menu."""

    options: list[SelectOption] | None = None
    """Specified choices in a select menu."""

    placeholder: str | None = None
    """Placeholder text if nothing is selected or default."""

    min_values: int | None = None
    """Minimum number of items that must be chosen. Discord defaults to `1`."""

    max_values: int | None = None
    """Maximum number of items that can be chosen. Discord defaults to `1`."""

    required: bool | None = None
    """Whether the string select is required to answer in a modal. Discord defaults to `True`."""

    disabled: bool | None = None # does not work on Modals!
    """Whether select menu is disabled in a message. Discord defaults to `False`."""

    type: ComponentType = field(init=False, default=ComponentType.STRING_SELECT)
    """Component type. Always `ComponentType.STRING_SELECT` for this class."""


@dataclass
class DefaultValue(DataModel):
    """Represents the Default Value for Select components."""

    id: Snowflake | None = None
    """ID of role, user, or channel."""

    type: DefaultValueType | None = None
    """Type of value that `id` represents."""

@dataclass
class SelectMenu(DataModel):
    """Represents common fields for Discord's select menus."""

    custom_id: str = None
    """ID for the select menu."""

    placeholder: str | None = None
    """Placeholder text if nothing is selected."""

    default_values: list[DefaultValue] | None = None
    """
        List of default values for auto-populated select menu components.
        Number of default values must be in the range of `min_values` to `max_values`.
    """

    min_values: int | None = None
    """Minimum number of items that must be chosen. Discord defaults to `1`."""

    max_values: int | None = None
    """Maximum number of items that can be chosen. Discord defaults to `1`."""

    required: bool | None = None
    """Whether the select is required to answer in a modal. Discord defaults to `True`."""

    disabled: bool | None = None
    """Whether select menu is disabled in a message. Discord defaults to `False`."""

@dataclass
class UserSelect(SelectMenu, Component, ActionRowChild, LabelChild):
    """Represents the User Select component.
    
    User Select allows users to select one or more users.
    """

    type: ComponentType = field(init=False, default=ComponentType.USER_SELECT)
    """Component type. Always `ComponentType.USER_SELECT` for this class."""

@dataclass
class RoleSelect(SelectMenu, Component, ActionRowChild, LabelChild):
    """Represents the Role Select component.
    
    A Role Select allows users to select one or more roles
    """

    type: ComponentType = field(init=False, default=ComponentType.ROLE_SELECT)
    """Component type. Always `ComponentType.ROLE_SELECT` for this class."""

@dataclass
class MentionableSelect(SelectMenu, Component, ActionRowChild, LabelChild):
    """Represents the Mentionable Select component.
    
    A Mentionable Select allows users to select one or more mentionables.
    """

    type: ComponentType = field(init=False, default=ComponentType.MENTIONABLE_SELECT)
    """Component type. Always `ComponentType.MENTIONABLE_SELECT` for this class."""

@dataclass
class ChannelSelect(SelectMenu, Component, ActionRowChild, LabelChild):
    """Represents the Channel Select component.
    
    A Channel Select allows users to select one or more channels.
    """

    type: ComponentType = field(init=False, default=ComponentType.CHANNEL_SELECT)
    """Component type. Always `ComponentType.CHANNEL_SELECT` for this class."""

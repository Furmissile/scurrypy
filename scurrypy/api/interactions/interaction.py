from dataclasses import dataclass, field

from ...core.model import DataModel
from ...core.snowflake import Snowflake
from ...core.exceptions import OptionNotFound
from ...core.types import HTTPResponse

from ...bases.interaction import InteractionData

from ...enums.permissions import Permissions
from ...enums.interaction import InteractionCallbackType, InteractionType
from ...enums.command import CommandType, CommandOptionType
from ...enums.components import ComponentType

from ..channels.channel import ChannelModel
from ..guilds.guild import GuildModel
from ..messages.message import MessageModel

from ..user import GuildMemberModel

from .resolved import ResolvedDataModel

from typing import Any, Self

@dataclass
class InteractionCallbackDataModel(DataModel):
    """Represents the interaction callback object."""

    id: Snowflake
    """ID of the interaction."""

    type: InteractionCallbackType
    """Type of interaction."""

    activity_instance_id: str
    """Instance ID of activity if an activity was launched or joined."""

    response_message_id: Snowflake
    """ID of the message created by the interaction."""

    response_message_loading: bool
    """If the interaction is in a loading state."""

    response_message_ephemeral: bool
    """If the interaction is ephemeral."""

@dataclass
class InteractionCallbackModel(DataModel):
    """Represents the interaction callback response object."""

    interaction: InteractionCallbackDataModel
    """The interaction object associated with the interaction response."""

@dataclass
class InteractionModel(DataModel):
    """Represents the interaction model."""

    type: InteractionType
    """Type of interaction."""

    id: Snowflake
    """ID of interaction."""

    token: str
    """token of interaction."""

    channel_id: Snowflake
    """ID of the channel where the interaction was sent."""

    application_id: Snowflake
    """ID of the application that owns the interaction."""

    app_permissions: Permissions
    """Bitwise set of permissions pertaining to the location of the interaction. [`INT_LIMIT`]"""

    member: GuildMemberModel
    """Guild member invoking the interaction."""

    message: MessageModel | None
    """Message associated with interaction (components or modals)."""

    guild_id: Snowflake | None
    """ID of guild the interaction was invoked (if invoked in a guild)."""

    guild: GuildModel | None
    """Partial guild object of the guild the interaction was invoked (if invoked in a guild)."""

    channel: ChannelModel | None
    """Partial channel object the interaction was invoked."""

# ----- Command Interaction -----

@dataclass
class ApplicationCommandOptionDataModel(DataModel):
    """Represents the response options from a slash command."""
    
    name: str
    """Name of the command option."""

    type: CommandOptionType
    """Type of command option."""

    value: str
    """
    Raw value from Discord as a string.
    
    Convert based on option type:
        - INTEGER/USER/CHANNEL/ROLE/ATTACHMENT: int(value)
        - NUMBER: float(value)  
        - BOOLEAN: value.lower() == 'true'

    otherwise the value is expected to be str
    """

    focused: bool
    """Whether this option is the currently focused option for autocomplete."""

@dataclass
class CommandDataModel(InteractionData):
    """Represents common command interaction data fields."""
    
    id: Snowflake
    """ID of the command."""

    name: str
    """Name of the command."""
    
    type: CommandType
    """Type of command (e.g., message, user, slash)."""

    guild_id: Snowflake | None
    """ID of guild from which the command was invoked."""

    target_id: Snowflake  | None
    """ID of the user or message from which the command was invoked (message/user commands only)."""

    resolved: ResolvedDataModel | None
    """Converted users + roles + channels + attachments."""

    options: list[ApplicationCommandOptionDataModel] = field(default_factory=list)
    """Options of the command (slash command only)."""

    def get_focused_value(self) -> str:
        """Get the next focused value in options.

        Returns:
            (str): next focused value or an empty string if no values are focused
        """
        if not self.options:
            return ""

        opt = next((o for o in self.options if o.focused), None)

        return opt.value if opt else ""

    def get_option(self, option_name: str) -> int | float | bool | str | None:
        """Get the input for a command option by name and convert it to its proper type.

        Args:
            option_name (str): option to fetch input from

        Returns:
            (int | float | bool | str | None): converted input data of specified option
        """
        for option in self.options:
            if option.name != option_name:
                continue

            if option.type in [
                CommandOptionType.INTEGER,
                CommandOptionType.USER,
                CommandOptionType.CHANNEL,
                CommandOptionType.ROLE,
                CommandOptionType.ATTACHMENT
            ]:
                return int(option.value)
            
            if option.type == CommandOptionType.NUMBER:
                return float(option.value)
            
            if option.type == CommandOptionType.BOOLEAN:
                return option.value.lower() == 'true'
            
            return option.value
        
        return None

@dataclass
class ApplicationCommandDataModel(CommandDataModel):
    """Represents the response from a command."""
    pass


@dataclass
class AutocompleteApplicationCommandDataModel(CommandDataModel):
    """Represents the response from an autocomplete command."""
    pass

# ----- Component Interaction -----

@dataclass
class MessageComponentDataModel(InteractionData):
    """Represents the select response from a select component."""

    custom_id: str
    """Unique ID associated with the component."""

    component_type: ComponentType
    """Type of component."""

    resolved: ResolvedDataModel | None
    """Resolved entities from selected options."""

    values: list[str] | None
    """Select values (if any)."""

# ----- Modal Interaction -----

@dataclass
class ModalComponentDataModel(DataModel):
    """Represents the modal field response from a modal."""

    type: ComponentType
    """Type of component."""
    
    custom_id: str
    """Unique ID associated with the component."""

@dataclass
class ModalComponentInputDataModel(ModalComponentDataModel):
    """Represents modal component variants with the value field."""

    value: str
    """Text input value.
    
    Convert based on option type:
        - CHECKBOX: value.lower() == 'true'

    otherwise the value is expected to be str
    """

@dataclass 
class ModalComponentSelectDataModel(ModalComponentDataModel):
    """Represents modal component variants with the values field."""
    
    values: list[str]
    """String select values."""

@dataclass
class ModalComponentModel(DataModel):
    """Represents the modal component response from a modal."""

    component: ModalComponentDataModel = field(init=False)
    """Data associated with the component."""

    @classmethod
    def from_dict(cls, data: HTTPResponse) -> Self:
        assert isinstance(data, dict)

        obj = super().from_dict(data)

        component_data = data.get("component")
        assert isinstance(component_data, dict)
        component_type = component_data.get("type")

        if component_type in {
            ComponentType.STRING_SELECT, 
            ComponentType.USER_SELECT, 
            ComponentType.ROLE_SELECT, 
            ComponentType.MENTIONABLE_SELECT, 
            ComponentType.CHANNEL_SELECT,
            ComponentType.FILE_UPLOAD,
            ComponentType.CHECKBOX_GROUP
        }:
            obj.component = ModalComponentSelectDataModel.from_dict(component_data)
        else:
            obj.component = ModalComponentInputDataModel.from_dict(component_data)

        return obj

@dataclass
class ModalDataModel(InteractionData):
    """Represents the modal response from a modal."""
    
    custom_id: str
    """Unique ID associated with the modal."""

    resolved: ResolvedDataModel | None
    """Resolved entities from modal data."""

    components: list[ModalComponentModel]
    """Components on the modal."""

    def get_modal_data(self, custom_id: str) -> bool | str | list[str]:
        """Fetch a modal field's data by its custom ID

        Args:
            custom_id (str): custom ID of field to fetch

        Raises:
            (OptionNotFound): invalid custom ID

        Returns:
            (bool | str | list[str]): component values (if select component) or value or bool if checkbox
        """

        for component in self.components:
            if custom_id != component.component.custom_id:
                continue

            if isinstance(component.component, ModalComponentInputDataModel):
                if component.component.type == ComponentType.CHECKBOX:
                    return component.component.value.lower() == 'true'
                return component.component.value
        
            if isinstance(component.component, ModalComponentSelectDataModel):
                return component.component.values

        raise OptionNotFound(f"Component custom ID '{custom_id}' not found.")

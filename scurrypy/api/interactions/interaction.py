from dataclasses import dataclass

from ...core.model import DataModel
from ...core.snowflake import Snowflake

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
class CommandDataModel(DataModel, InteractionData):
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

    options: list[ApplicationCommandOptionDataModel] | None
    """Options of the command (slash command only)."""

    def get_focused_value(self):
        opt = next((opt for opt in self.options if opt), None)
        
        return opt.value if opt else ""

    def get_option(self, option_name: str, default = None):
        """Get the input for a command option by name and convert it to its proper type.

        Args:
            option_name (str): option to fetch input from

        Returns:
            (int | float | bool | str | Any): converted input data of specified option
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
        
        return default

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
class MessageComponentDataModel(DataModel, InteractionData):
    """Represents the select response from a select component."""

    custom_id: str
    """Unique ID associated with the component."""

    component_type: int
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
    
    value: str | None
    """Text input value.
    
    Convert based on option type:
        - CHECKBOX: value.lower() == 'true'

    otherwise the value is expected to be str
    """

    custom_id: str
    """Unique ID associated with the component."""

    values: list[str] | None
    """String select values."""

@dataclass
class ModalComponentModel(DataModel):
    """Represents the modal component response from a modal."""

    type: ComponentType
    """Type of component."""

    component: ModalComponentDataModel
    """Data associated with the component."""

@dataclass
class ModalDataModel(DataModel, InteractionData):
    """Represents the modal response from a modal."""
    
    custom_id: str
    """Unique ID associated with the modal."""

    resolved: ResolvedDataModel | None
    """Resolved entities from modal data."""

    components: list[ModalComponentModel]
    """Components on the modal."""

    def get_modal_data(self, custom_id: str):
        """Fetch a modal field's data by its custom ID

        Args:
            custom_id (str): custom ID of field to fetch

        Raises:
            (ValueError): invalid custom ID

        Returns:
            (str, list[str], bool): component values (if select component) or value or bool if checkbox
        """
        from ...enums.components import ComponentType
        
        for component in self.components:
            if custom_id != component.component.custom_id:
                continue

            t = component.component.type

            if t in [
                ComponentType.STRING_SELECT, 
                ComponentType.USER_SELECT, 
                ComponentType.ROLE_SELECT, 
                ComponentType.MENTIONABLE_SELECT, 
                ComponentType.CHANNEL_SELECT,
                ComponentType.FILE_UPLOAD,
                ComponentType.CHECKBOX_GROUP
            ]:
                return component.component.values
            
            if t == ComponentType.CHECKBOX: # value is bool for checkboxes
                return component.component.value.lower() == 'true'
            
            # text input
            return component.component.value

        raise ValueError(f"Component custom ID '{custom_id}' not found.")

from dataclasses import dataclass, field
from typing import Optional
from ..model import DataModel

from ..resources.interaction import Interaction

# ----- Command Interaction -----

@dataclass
class ApplicationCommandOptionData(DataModel):
    """Represents the response options from a slash command."""
    name: str
    """Name of the command option."""

    type: int
    """Type of command option. See [`CommandOptionTypes`][discord.parts.command.CommandOptionTypes]."""

    value: str | int | float | bool
    """Input value for option."""

@dataclass
class ApplicationCommandData(DataModel):
    """Represents the response from a command."""
    id: int
    """ID of the command."""

    name: str
    """Name of the command."""
    
    type: int
    """Type of command (e.g., message, user, slash)."""

    guild_id: Optional[int]
    """ID of guild from which the command was invoked."""

    target_id: Optional[int]
    """ID of the user or message from which the command was invoked (message/user commands only)."""

    options: Optional[list[ApplicationCommandOptionData]] = field(default_factory=list)
    """Options of the command (slash command only)."""

    def get_command_option_value(self, option_name: str):
        """Get the input for a command option by name.

        Args:
            option_name (str): option to fetch input from

        Raises:
            ValueError: invalid option name

        Returns:
            (str | int | float | bool): input data of specified option
        """
        for option in self.options:
            if option_name != option.name:
                continue

            return option.value
        
        raise ValueError(f"Option name '{option_name}' could not be found.")

# ----- Component Interaction -----

@dataclass
class MessageComponentData(DataModel):
    """Represents the select response from a select component."""

    custom_id: str
    """Unique ID associated with the component."""

    component_type: int
    """Type of component."""

    values: Optional[list[str]] = field(default_factory=list)
    """Select values (if any)."""

# ----- Modal Interaction -----

@dataclass
class ModalComponentData(DataModel):
    """Represents the modal field response from a modal."""
    type: int
    """Type of component."""
    
    value: Optional[str]
    """Text input value (Text Input component only)."""

    values: Optional[list[str]]
    """String select values (String Select component only)."""

    custom_id: str
    """Unique ID associated with the component."""

@dataclass
class ModalComponent(DataModel):
    """Represents the modal component response from a modal."""
    type: int
    """Type of component."""

    component: ModalComponentData
    """Data associated with the component."""

@dataclass
class ModalData(DataModel):
    """Represents the modal response from a modal."""
    
    custom_id: str
    """Unique ID associated with the modal."""

    components: list[ModalComponent] = field(default_factory=list)
    """Components on the modal."""

    def get_modal_data(self, custom_id: str):
        """Fetch a modal field's data by its custom ID

        Args:
            custom_id (str): custom ID of field to fetch

        Raises:
            ValueError: invalid custom ID

        Returns:
            (str | list[str]): component values (if string select) or value (if text input)
        """
        for component in self.components:
            if custom_id != component.component.custom_id:
                continue

            match component.component.type:
                case 3: # string select -> values
                    return component.component.values
                case 4: # text input -> value
                    return component.component.value

        raise ValueError(f"Component custom id '{custom_id}' not found.")

@dataclass
class InteractionEvent(DataModel):
    """Represents the interaction response."""

    interaction: Interaction
    """Interaction resource object. See [`Interaction`][discord.resources.interaction.Interaction]."""

    data: Optional[ApplicationCommandData | MessageComponentData | ModalData] = None
    """Interaction response data."""

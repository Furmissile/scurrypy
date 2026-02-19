from dataclasses import dataclass

from ...core.model import DataModel
from ...core.snowflake import Snowflake

from ...enums.permissions import Permissions
from ...enums.command import CommandOptionType, CommandType

@dataclass
class ApplicationCommandOptionChoiceModel(DataModel):
    """Represents the application command option choice object."""

    name: str
    """Name of the choice."""

    value: str
    """Value for the choice.
    
    !!! note
        Convert based on expected type (str, int or double)
    """

@dataclass
class ApplicationCommandOptionModel(DataModel):
    """Represents the application command option object."""

    type: CommandOptionType
    """Type of command option."""

    name: str
    """Name of the command option."""

    descripton: str
    """Description for the command option."""
    
    required: bool | None
    """Whether this option is required. Discord defaults to `False`."""

    choices: list[ApplicationCommandOptionChoiceModel] | None
    """Choices for the user to pick from."""

    channel_types: list[int] | None
    """Channels shown will be restricted to these types."""

    min_value: int | None
    """Minimum value allowed."""

    max_value: int | None
    """Maximum value allowed."""

    min_length: int | None
    """Minimum length allowed."""

    max_length: int | None
    """Maximum length allowed."""

    autocomplete: bool | None
    """Whether autocomplete interactions are enabled for this option."""

@dataclass
class ApplicationCommandModel(DataModel):
    """Represents the application command object."""

    id: Snowflake
    """Unique ID of command."""

    type: CommandType | None
    """Type of command. Discord defaults to `ApplicationCommandTypes.CHAT_INPUT`."""

    application_id: Snowflake
    """ID of the parent application."""

    guild_id: Snowflake | None
    """Guild ID of the command, if not global."""

    name: str
    """Name of the command."""

    description: str
    """Description for `CHAT_INPUT` commands. 
    
    !!! note
        Empty for `USER` and `MESSAGE` commands.
    """

    options: list[ApplicationCommandOptionModel] | None
    """Parameters for the command."""

    default_member_permissions: Permissions
    """Set of permissions represented as a bit set. [`INT_LIMIT`]"""

    nsfw: bool | None
    """Whether the command is age-restricted. Discord defaults to `False`."""

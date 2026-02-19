from dataclasses import dataclass, field

from ...core.model import DataModel

from ...enums.command import CommandOptionType, CommandType

@dataclass
class CommandOptionChoicePart(DataModel):
    """Choice for a command option."""

    name: str | None = None
    """Name of the choice."""

    value: str | int | float | None = None
    """Value for the user to select (same as option type)."""

    name_localizations: dict | None = None
    """Dictionary with keys in available locales."""

@dataclass
class CommandOptionPart(DataModel):
    """Option for a slash command."""

    type: CommandOptionType | None = None
    """Type of option."""

    name: str | None = None
    """Name of option."""

    description: str | None = None
    """Description of option."""

    required: bool | None = None
    """Whether this option is required. Discord defaults to `False`."""

    choices: list[CommandOptionChoicePart] | None = None
    """Choices for the user to pick from, max 25. Only valid for STRING, INTEGER, NUMBER option types."""

    autocomplete: bool | None = None
    """Whether autocomplete interactions are enabled for this option. Discord defaults to `False`."""

@dataclass
class SlashCommandPart(DataModel):
    """Represents the slash command object."""

    name: str | None = None
    """Name of the command."""

    description: str | None = None
    """Description of the command."""

    options: list[CommandOptionPart] | None = None
    """Parameters or options for the command."""

    type: CommandType = field(init=False, default=CommandType.CHAT_INPUT)
    """Command type. Always `CommandType.CHAT_INPUT` for this class."""

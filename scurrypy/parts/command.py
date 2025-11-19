from dataclasses import dataclass, field

from ..core.model import DataModel

class CommandTypes:
    CHAT_INPUT = 1
    USER_COMMAND = 2
    MESSAGE_COMMAND = 3

class CommandOptionTypes:
    """Slash command option input types."""

    STRING = 3
    """string (text)"""

    INTEGER = 4
    """integer (whole)"""

    BOOLEAN = 5
    """boolean (true/false)"""

    USER = 6
    """user pangination"""

    CHANNEL = 7
    """channel pangination"""

    ROLE = 8
    """role pangination"""

    MENTIONABLE = 9
    """any pangination (role, channel, user)"""

    NUMBER = 10
    """number (float, integer)"""

    ATTACHMENT = 11
    """file upload"""

@dataclass
class CommandOption(DataModel):
    """Option for a slash command."""

    type: int
    """Type of option. See [`CommandOptionTypes`][scurrypy.parts.command.CommandOptionTypes]."""

    name: str
    """Name of option."""

    description: str
    """Description of option."""

    required: bool = False
    """Whether this option is required. Defaults to False."""

@dataclass
class SlashCommand(DataModel):
    """Represents the slash command object."""

    name: str
    """Name of the command."""

    description: str
    """Description of the command."""

    options: list[CommandOption] = field(default_factory=list)
    """Parameters or options for the command."""

    type: int = field(init=False, default=CommandTypes.CHAT_INPUT)
    """Command type. Always `CommandTypes.CHAT_INPUT` for this class. See [`CommandTypes`][scurrypy.parts.command.CommandTypes]."""

@dataclass
class UserCommand(DataModel):
    """Represents the user command object"""

    name: str
    """Name of the command."""

    type: int = field(init=False, default=CommandTypes.USER_COMMAND)
    """Command type. Always `CommandTypes.USER_COMMAND` for this class. See [`CommandTypes`][scurrypy.parts.command.CommandTypes]."""

@dataclass
class MessageCommand(DataModel):
    """Represents the message command object."""
    
    name: str
    """Name of the command."""

    type: int = field(init=False, default=CommandTypes.MESSAGE_COMMAND)
    """Command type. Always `CommandTypes.MESSAGE_COMMAND` for this class. See [`CommandTypes`][scurrypy.parts.command.CommandTypes]."""

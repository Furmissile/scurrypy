from dataclasses import dataclass, field
from typing import Literal

from ..model import DataModel

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
class MessageCommand(DataModel):
    """Represents the message command object."""
    type: Literal[3] = field(init=False, default=3) # MESSAGE
    name: str

@dataclass
class UserCommand(DataModel):
    """Represents the user command object"""
    type: Literal[2] = field(init=False, default=2) # USER
    name: str

@dataclass
class _CommandOption(DataModel):
    """Option for a slash command."""
    type: int   # refer to CommandOptionTypes
    name: str
    description: str
    required: bool = True

@dataclass
class SlashCommand(DataModel):
    type: Literal[1] = field(init=False, default=1) # CHAT_INPUT
    name: str
    description: str
    options: list[_CommandOption] = field(default_factory=list)

    def add_option(
        self,
        command_type: Literal['String', 'Integer', 'Boolean', 'User', 'Channel', 'Role', 'Mentionable', 'Number', 'Attachment'],
        name: str,
        description: str,
        required: bool = False
    ):
        """Add an option to this slash command.

        Args:
            command_type (Literal['String', 'Integer', 'Boolean', 'User', 'Channel', 'Role', 'Mentionable', 'Number', 'Attachment']): 
                input type for the option
            name (str): name of the option
            description (str): description for the option
            required (bool, optional): if the option is required. Defaults to False.

        Returns:
            (SlashCommand): self
        """
        _command_types = {
            'STRING': CommandOptionTypes.STRING,
            'INTEGER': CommandOptionTypes.INTEGER,
            'BOOLEAN': CommandOptionTypes.BOOLEAN,
            'USER': CommandOptionTypes.BOOLEAN,
            'CHANNEL': CommandOptionTypes.CHANNEL,
            'ROLE': CommandOptionTypes.ROLE,
            'MENTIONABLE': CommandOptionTypes.MENTIONABLE,
            'NUMBER': CommandOptionTypes.NUMBER,
            'ATTACHMENT': CommandOptionTypes.ATTACHMENT
        }

        self.options.append(
            _CommandOption(
                type=_command_types.get(command_type.upper()), 
                name=name, 
                description=description, 
                required=required
            )
        )
        return self

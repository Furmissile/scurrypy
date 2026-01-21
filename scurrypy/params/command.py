from typing import TypedDict, Optional

from ..parts.command import CommandOption

class EditGuildCommandParams(TypedDict):
    """Parameters for editing a guild command."""

    name: Optional[str]
    """Name of the command."""

    description: Optional[str]
    """Description for the command."""

    options: Optional[list[CommandOption]]
    """Options with the command."""

    nsfw: Optional[bool]
    """Whether this command is age restricted."""

class EditGlobalCommandParams(TypedDict):
    """Parameters for editing a global command."""

    name: Optional[str]
    """Name of the command."""

    description: Optional[str]
    """Description for the command."""

    options: Optional[list[CommandOption]]
    """Options with the command."""

    nsfw: Optional[bool]
    """Whether this command is age restricted."""

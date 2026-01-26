from typing import TypedDict, Optional

from ..parts.command import CommandOptionPart

class EditGuildCommandParams(TypedDict, total=False):
    """Parameters for editing a guild command."""

    name: Optional[str]
    """Name of the command."""

    description: Optional[str]
    """Description for the command."""

    options: Optional[list[CommandOptionPart]]
    """Options with the command."""

    nsfw: Optional[bool]
    """Whether this command is age restricted."""

class EditGlobalCommandParams(TypedDict, total=False):
    """Parameters for editing a global command."""

    name: Optional[str]
    """Name of the command."""

    description: Optional[str]
    """Description for the command."""

    options: Optional[list[CommandOptionPart]]
    """Options with the command."""

    nsfw: Optional[bool]
    """Whether this command is age restricted."""

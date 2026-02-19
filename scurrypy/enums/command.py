from .enum_types import DiscordTypes

class CommandType(DiscordTypes):
    """Types of commands."""
    
    CHAT_INPUT = 1
    """Slash commands; a text-based command that shows up when a user types `/`."""

    USER = 2
    """A UI-based command that shows up when you right click or tap on a user."""
    
    MESSAGE = 3
    """A UI-based command that shows up when you right click or tap on a message."""

class CommandOptionType(DiscordTypes):
    """Slash command option input types."""

    STRING = 3
    """string (text)"""

    INTEGER = 4
    """integer (Any integer between -2^53+1 and 2^53-1)"""

    BOOLEAN = 5
    """boolean (true/false)"""

    USER = 6
    """user pangination"""

    CHANNEL = 7
    """channel pangination (category and channels)"""

    ROLE = 8
    """role pangination"""

    MENTIONABLE = 9
    """any pangination (role and user)"""

    NUMBER = 10
    """number (Any double between -2^53 and 2^53)"""

    ATTACHMENT = 11
    """File upload. See [`AttachmentPart`][scurrypy.api.messages.AttachmentPart]."""

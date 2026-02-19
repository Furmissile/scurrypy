from .enum_types import DiscordTypes, DiscordString

class ComponentType(DiscordTypes):
    ACTION_ROW = 1
    BUTTON = 2
    STRING_SELECT = 3
    TEXT_INPUT = 4
    USER_SELECT = 5
    ROLE_SELECT = 6
    MENTIONABLE_SELECT = 7
    CHANNEL_SELECT = 8
    SECTION = 9
    TEXT_DISPLAY = 10
    THUMBNAIL = 11
    MEDIA_GALLERY = 12
    FILE = 13
    SEPARATOR = 14
    CONTAINER = 17
    LABEL = 18
    FILE_UPLOAD = 19
    RADIO_GROUP = 21
    CHECKBOX_GROUP = 22
    CHECKBOX = 23

class SeparatorType(DiscordTypes):
    """Represents separator types constants."""

    SMALL_PADDING = 1
    """Small separator padding."""
    
    LARGE_PADDING = 2
    """Large separator padding."""

class ButtonStyle(DiscordTypes):
    """Represents button styles for a Button component."""

    PRIMARY = 1
    """The most important or recommended action in a group of options. (Blurple)"""

    SECONDARY = 2
    """Alternative or supporting actions. (Gray)"""

    SUCCESS = 3
    """Positive confirmation or completion actions. (Green)"""

    DANGER = 4
    """An action with irreversible consequences. (Red)"""

    LINK = 5
    """Navigates to a URL. (Gray + window)"""

class TextInputStyle(DiscordTypes):
    """Represents the types of Text Inputs."""

    SHORT = 1
    """One line text input."""

    PARAGRAPH = 2
    """Multi-line text input."""

class DefaultValueType(DiscordString):
    ROLE = "role"
    CHANNEL = "channel"
    USER = "user"

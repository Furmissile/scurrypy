from enum import IntFlag, IntEnum, StrEnum

class DiscordTypes(IntEnum):
    """Base class for Discord's types."""
    @classmethod
    def from_dict(cls, v):
        return cls(int(v))
    
class DiscordFlags(IntFlag):
    """Base class for Discord's flags."""
    @classmethod
    def from_dict(cls, v):
        return cls(int(v))

class DiscordString(StrEnum):
    """Base class for Discord's pre-defined strings."""
    @classmethod
    def from_dict(cls, v):
        return cls(str(v))

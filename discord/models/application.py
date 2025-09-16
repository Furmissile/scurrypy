from dataclasses import dataclass
from ..model import DataModel
from .user import UserModel
from .guild import GuildModel

@dataclass
class ApplicationModel(DataModel):
    """Represents a bot application object."""
    id: int
    """ID of the app."""

    name: str
    """Name of the app."""

    icon: str
    """Icon hash of the app."""

    description: str
    """Description of the app."""

    bot_public: bool
    """If other users can add this app to a guild."""

    bot: UserModel
    """Partial user obhect for the bot user associated with the app."""

    owner: UserModel
    """Partial user object for the owner of the app."""

    guild_id: int
    """Guild ID associated with the app (e.g., a support server)."""

    guild: GuildModel
    """Partial guild object of the associated guild."""

    approximate_guild_count: int
    """Approximate guild member count."""

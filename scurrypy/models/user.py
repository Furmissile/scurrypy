from dataclasses import dataclass
from ..core.model import DataModel

from .guild import GuildModel

from typing import Optional

@dataclass
class UserModel(DataModel):
    """Describes the User object."""
    id: int
    """ID of the user."""

    username: str
    """Username of the user."""

    avatar: str
    """Avatar hash of the user."""

@dataclass
class MemberModel(DataModel):
    """Represents a guild member."""

    roles: list[int]
    """List of roles registered to the guild member."""

    user: UserModel
    """User data associated with the guild member."""

    nick: str
    """Server nickname of the guild member."""

    avatar: str
    """Server avatar hash of the guild mmeber."""

    joined_at: str
    """ISO8601 timestamp of when the guild member joined server."""

    deaf: bool
    """If the member is deaf in a VC (input)."""

    mute: bool
    """If the member is muted in VC (output)."""

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

@dataclass
class IntegrationModel(DataModel):
    """Represents a guild integration."""

    id: int
    """ID of the integration."""

    name: str
    """Name of the integration."""

    type: str
    """Type of integration (e.g., twitch, youtube, discord, or guild_subscription)."""

    enabled: bool
    """If the integration is enabled."""

    application: Optional[ApplicationModel] = None
    """The bot aaplication for Discord integrations."""

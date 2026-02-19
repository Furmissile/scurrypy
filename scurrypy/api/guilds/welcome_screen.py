from dataclasses import dataclass

from ...core.model import DataModel
from ...core.snowflake import Snowflake

@dataclass
class GuildWelcomeChannelModel(DataModel):
    """Represents channels shown on a welcome screen."""

    channel_id: Snowflake
    """ID of the channel."""

    description: str
    """Description for the channel."""

    emoji_id: Snowflake
    """Emoji ID for the welcome screen (if custom)."""

    emoji_name: str
    """Emoji name for the welcome screen."""

@dataclass
class GuildWelcomeScreenModel(DataModel):
    """Represents a guild's welcome screen."""

    description: str
    """Guild description displayed."""

    welcome_channels: list[GuildWelcomeChannelModel]
    """Channels displayed on the welcome screen. Max `5`."""

@dataclass
class WelcomeScreenChannelPart(DataModel):
    """Represents fields for creating a welcome screen channel."""

    channel_id: Snowflake | None = None
    """ID of the channel to display."""

    description: str | None = None
    """Description for the channel to display."""

    emoji_id: Snowflake | None = None
    """ID of the emoji (if custom)."""

    emoji_name: str | None = None
    """Name of the emoji."""

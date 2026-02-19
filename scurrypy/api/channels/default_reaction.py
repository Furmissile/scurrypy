from dataclasses import dataclass

from ...core.model import DataModel
from ...core.snowflake import Snowflake

@dataclass
class DefaultReactionModel(DataModel):
    """Represents the default reaction for a `GUILD_FORUM` post."""

    emoji_id: Snowflake
    """ID of the guild's custom emoji."""

    emoji_name: str
    """Unicode character of the emoji."""

@dataclass
class DefaultReactionPart(DataModel):
    """Represents the default reaction for a `GUILD_FORUM` post."""

    emoji_id: int | None = None
    """ID of the guild's custom emoji."""

    emoji_name: str | None = None
    """Unicode character of the emoji."""

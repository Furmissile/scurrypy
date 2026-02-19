from dataclasses import dataclass

from ...core.model import DataModel
from ...core.snowflake import Snowflake

from ..emoji import EmojiModel
from .role import GuildRoleModel

@dataclass
class ReadyGuildModel(DataModel):
    """Guild info from Ready event."""
    
    id: Snowflake
    """ID of the associated guild."""

    unavailable: bool
    """If the guild is offline."""

@dataclass
class UnavailableGuildModel(DataModel):
    """Guild info during an outage or before bot bootup."""

    id: Snowflake
    """ID of the associated guild."""

    unavailable: bool
    """If the guild is offline."""

@dataclass
class GuildModel(DataModel):
    """Represents a Discord guild."""

    id: Snowflake
    """ID of the guild."""
    
    name: str
    """Name of the guild."""

    icon: str
    """Image hash of the guild's icon."""

    splash: str
    """Image hash of the guild's splash."""

    owner: bool | None
    """If the member is the owner."""

    owner_id: Snowflake
    """OD of the owner of the guild."""

    roles: list[int]
    """List of IDs registered in the guild."""

    emojis: list[EmojiModel]
    """List of emojis registered in the guild."""

    roles: list[GuildRoleModel]
    """Roles in the guild."""

    mfa_level: int
    """Required MFA level of the guild."""

    application_id: Snowflake
    """ID of the application if the guild is created by a bot."""

    system_channel_id: Snowflake
    """Channel ID where system messages go (e.g., welcome messages, boost events)."""

    system_channel_flags: int
    """System channel flags."""

    rules_channel_id: Snowflake
    """Channel ID where rules are posted."""

    max_members: int | None
    """Maximum member capacity for the guild."""

    description: str
    """Description of the guild."""

    banner: str
    """Image hash of the guild's banner."""

    preferred_locale: str
    """Preferred locale of the guild."""

    public_updates_channel_id: Snowflake
    """Channel ID of announcement or public updates."""

    approximate_member_count: int
    """Approximate number of members in the guild."""

    nsfw_level: int
    """NSFW level of the guild."""

    safety_alerts_channel_id: Snowflake
    """Channel ID for safety alerts."""

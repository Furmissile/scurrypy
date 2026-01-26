from dataclasses import dataclass
from ..core.model import DataModel

from typing import Optional

from .emoji import EmojiModel
from .role import RoleModel
from .user import UserModel

class GuildFeatures:
    NEWS = "NEWS"
    ROLE_ICONS = "ROLE_ICONS"
    ANIMATED_ICON = "ANIMATED_ICON"
    INVITE_SPLASH = "INVITE_SPLASH"
    DISCOVERABLE = "DISCOVERABLE"
    BANNER = "BANNER"
    ANIMATED_BANNER = "ANIMATED_BANNER"
    PARTNERED = "PARTNERED"

@dataclass
class ReadyGuildModel(DataModel):
    """Guild info from Ready event."""
    
    id: int
    """ID of the associated guild."""

    unavailable: bool
    """If the guild is offline."""

@dataclass
class UnavailableGuildModel(DataModel):
    """Guild info during an outage or before bot bootup."""

    id: int
    """ID of the associated guild."""

    unavailable: bool
    """If the guild is offline."""

@dataclass
class GuildModel(DataModel):
    """Represents a Discord guild."""

    id: int
    """ID of the guild."""
    
    name: str
    """Name of the guild."""

    icon: str
    """Image hash of the guild's icon."""

    splash: str
    """Image hash of the guild's splash."""

    owner: Optional[bool]
    """If the member is the owner."""

    owner_id: int
    """OD of the owner of the guild."""

    roles: list[int]
    """List of IDs registered in the guild."""

    emojis: list[EmojiModel]
    """List of emojis registered in the guild."""

    roles: list[RoleModel]
    """Roles in the guild."""

    mfa_level: int
    """Required MFA level of the guild."""

    application_id: int
    """ID of the application if the guild is created by a bot."""

    system_channel_id: int
    """Channel ID where system messages go (e.g., welcome messages, boost events)."""

    system_channel_flags: int
    """System channel flags."""

    rules_channel_id: int
    """Channel ID where rules are posted."""

    max_members: Optional[int]
    """Maximum member capacity for the guild."""

    description: str
    """Description of the guild."""

    banner: str
    """Image hash of the guild's banner."""

    preferred_locale: str
    """Preferred locale of the guild."""

    public_updates_channel_id: int
    """Channel ID of announcement or public updates."""

    approximate_member_count: int
    """Approximate number of members in the guild."""

    nsfw_level: int
    """NSFW level of the guild."""

    safety_alerts_channel_id: int
    """Channel ID for safety alerts."""

@dataclass
class GuildBanModel(DataModel):
    """Represents the guild ban object."""

    reason: str
    """Reason for the ban."""
    
    user: UserModel
    """Banned user object."""

@dataclass
class BulkGuildBanModel(DataModel):
    """Response body for creating bulk guild bans."""

    banned_users: list[int]
    """IDs of successfully banned users."""

    failed_users: list[int]
    """IDs of users not banned."""

@dataclass
class GuildWelcomeChannelModel(DataModel):
    """Represents channels shown on a welcome screen."""

    channel_id: int
    """ID of the channel."""

    description: str
    """Description for the channel."""

    emoji_id: int
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
class OnboardingPromptOptionModel(DataModel):
    """Represents a guild's prompt option for onboarding."""

    id: int
    """ID of the prompt option."""

    channel_ids: list[int]
    """Channel IDs a member is added to when selected."""

    role_ids: list[int]
    """Role IDs a member is given when selected."""

    emoji: Optional[EmojiModel]
    """Emoji for the option."""

    emoji_id: Optional[int]
    """ID for the emoji of the option."""

    emoji_name: Optional[str]
    """Name for the emoji of the option."""

    emoji_animated: Optional[bool]
    """Whether the emoji of the option is animated."""

    title: str
    """Title of the option."""

    description: str
    """Description of the option."""

@dataclass
class OnboardingPromptModel(DataModel):
    """Represents a guild's prompt for onboarding."""

    id: int
    """ID of the prompt."""

    type: int
    """Type of prompt. See [`PromptTypes`][scurrypy.parts.guild.PromptTypes]."""

    options: list[OnboardingPromptOptionModel]
    """Options available with the prompt."""

    title: str
    """Title of the prompt."""

    single_select: bool
    """Whether users are limited to selecting one option."""

    required: bool
    """Whether the prompt is required for completing the onboarding process."""

    in_onboarding: bool
    """Whether the prompt is present in the onboarding flow."""

@dataclass
class GuildOnboadingModel(DataModel):
    """Represents a guild's onboarding flow."""

    guild_id: int
    """ID of the guild for onboarding."""

    prompts: list[OnboardingPromptModel]
    """Prompts shown during onboarding."""

    default_channel_ids: list[int]
    """Channel IDs members are opted into by default."""

    enabled: bool
    """Whether onboarding is enabled for the guild."""

    mode: int
    """Current mode of onboarding. See [`OnboardingModes`][scurrypy.parts.guild.OnboardingModes]."""

from typing import TypedDict, Optional

from ..parts.role import RoleColorsPart
from ..parts.image_data import ImageData
from ..parts.guild import WelcomeScreenChannelPart

class EditGuildParams(TypedDict, total=False):
    """Represents fields for editing a guild."""

    name: str
    """Guild name."""

    afk_channel_id: int
    """Channel ID for AFK channel."""

    icon: ImageData
    """Data URI scheme for guild icon.
    
    !!! note
        Can be animated if guild has `ANIMATED_ICON` feature.
    """

    splash: ImageData
    """Data URI scheme for guild splash if guild has `INVITE_SPLASH` feature."""

    discovery_splash: ImageData
    """Data URI scheme for guild discovery if guild has `DISCOVERABLE` feature."""

    banner: ImageData
    """Data URI scheme for guild banner if guild has `BANNER` feature.
    
    !!! note
        Can be animated if guild has `ANIMATED_BANNER` feature.
    """

    system_channel_id: int
    """Channel ID for receiving guild notices (e.g., boosts, user join)."""

    rules_channel_id: int
    """Channel ID for where guilds display rules."""

    public_updates_channel_id: int
    """Channel ID for receiving notices from Discord."""

    features: list[str]
    """Enabled guild features. See [`GuildFeatures`][scurrypy.models.guild.GuildFeatures]."""

    description: str
    """Description for the guild."""

    premium_progress_bar_enabled: bool
    """Whether the guild's boost progress bar should be shown."""

    safety_alerts_channel_id: int
    """Channel ID for receiving safety alerts from Discord."""

class EditGuildRoleParams(TypedDict, total=False):
    """Represents fields for editing a guild role."""

    name: Optional[str]
    """Name of the role."""

    colors: Optional[RoleColorsPart]
    """Colors of the role."""

    hoist: Optional[bool]
    """Whether the role is displayed separately on the sidebar."""

    icon: Optional[ImageData]
    """Icon of the role (if guild has `ROLE_ICONS` feature)."""

    permissions: int = None
    """Permission bit set. [`INT_LIMIT`]"""

    unicode_emoji: Optional[str]
    """Unicode emoji of the role (if guilde has `ROLE_ICONS` feature)."""

    mentionable: Optional[bool]
    """Whether the role should be mentionable."""

class EditGuildWelcomeScreen(TypedDict, total=False):
    """Represents fields for editing a guild welcome screen."""

    enabled: bool
    """Whether the welcome scren is enabled."""

    welcome_channels: list[WelcomeScreenChannelPart]
    """Channels linked when the welcome screen is displayed."""

    description: str
    """Guild description to show on the welcome screen."""

from dataclasses import dataclass, field
from ..core.model import DataModel

from typing import Optional

@dataclass
class BulkGuildBanPart(DataModel):
    """Represents fields for creating a bulk ban."""

    user_ids: list[int] = field(default_factory=list)
    """List of user IDs to ban. Max `200`."""

    delete_message_seconds: Optional[int] = 0
    """seconds back to delete messages. Max `604800` (7 days). Defaults to `0`."""

@dataclass
class WelcomeScreenChannelPart(DataModel):
    """Represents fields for creating a welcome screen channel."""

    channel_id: int = None
    """ID of the channel to display."""

    description: str = None
    """Description for the channel to display."""

    emoji_id: int = None
    """ID of the emoji (if custom)."""

    emoji_name: str = None
    """Name of the emoji."""

class PromptTypes:
    MULTIPLE_CHOICE = 0
    DROPDOWN = 1

class OnboardingModes:
    ONBOARDING_DEFAULT = 0
    ONBOARDING_ADVANCED = 1

@dataclass
class OnboardingPromptOptionPart(DataModel):
    """Represents fields for creating an onboarding prompt option."""

    channel_ids: list[int] = field(default_factory=list)
    """	IDs for channels a member is added to when the option is selected."""

    role_ids: list[int] = field(default_factory=list)
    """IDs for roles assigned to a member when the option is selected."""

    wmoji_id: Optional[int] = None
    """	Emoji ID of the option."""

    emoji_name: Optional[str] = None
    """Emoji name of the option."""

    emoji_animated: Optional[bool] = None
    """Whether the emoji is animated."""

    title: str = None
    """Title of the option."""

    description: str = None
    """Description of the option."""

@dataclass
class OnboardingPromptPart(DataModel):
    """Represents fields for creating an onboarding prompt."""

    type: int = None
    """Type of prompt. See [`PromptTypes`][scurrypy.parts.guild.PromptTypes]"""

    options: list[OnboardingPromptOptionPart] = field(default_factory=list)
    """Options available with the prompt."""

    title: str = None
    """Title of the prompt."""

    single_select: bool = None
    """Whether the users are limited to selecting one option."""

    required: bool = None
    """Whether the prompt is required to complete the onboarding flow."""

class StickerTypes:
    """Sticker types."""

    STANDARD = 1
    """An official sticker in a pack."""

    GUILD = 2
    """A sticker uploaded to a guild for the guild's members."""

class StickerFormatTypes:
    PNG = 1
    APNG = 2
    LOTTIE = 3
    GIF = 4

@dataclass
class GuildStickerPart(DataModel):
    """Represents fields for creating a guild sticker."""

    name: str = None
    """Name of the sticker."""

    description: str = None
    """Description of the sticker."""

    tags: str = None
    """Autocomplete/suggestion tags for the sticker."""

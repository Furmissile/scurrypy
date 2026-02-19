from dataclasses import dataclass

from ...core.model import DataModel
from ...core.snowflake import Snowflake

from ...enums.guild import OnboardingMode, PromptType

from ..emoji import EmojiModel

@dataclass
class OnboardingPromptOptionModel(DataModel):
    """Represents a guild's prompt option for onboarding."""

    id: Snowflake
    """ID of the prompt option."""

    channel_ids: list[Snowflake]
    """Channel IDs a member is added to when selected."""

    role_ids: list[Snowflake]
    """Role IDs a member is given when selected."""

    emoji: EmojiModel | None
    """Emoji for the option."""

    emoji_id: Snowflake | None
    """ID for the emoji of the option."""

    emoji_name: str | None
    """Name for the emoji of the option."""

    emoji_animated: bool | None
    """Whether the emoji of the option is animated."""

    title: str
    """Title of the option."""

    description: str
    """Description of the option."""

@dataclass
class OnboardingPromptModel(DataModel):
    """Represents a guild's prompt for onboarding."""

    id: Snowflake
    """ID of the prompt."""

    type: PromptType
    """Type of prompt."""

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

    guild_id: Snowflake
    """ID of the guild for onboarding."""

    prompts: list[OnboardingPromptModel]
    """Prompts shown during onboarding."""

    default_channel_ids: list[Snowflake]
    """Channel IDs members are opted into by default."""

    enabled: bool
    """Whether onboarding is enabled for the guild."""

    mode: OnboardingMode
    """Current mode of onboarding."""

@dataclass
class OnboardingPromptOptionPart(DataModel):
    """Represents fields for creating an onboarding prompt option."""

    channel_ids: list[Snowflake] | None = None
    """	IDs for channels a member is added to when the option is selected."""

    role_ids: list[Snowflake] | None = None
    """IDs for roles assigned to a member when the option is selected."""

    wmoji_id: Snowflake | None = None
    """	Emoji ID of the option."""

    emoji_name: str | None = None
    """Emoji name of the option."""

    emoji_animated: bool | None = None
    """Whether the emoji is animated."""

    title: str | None = None
    """Title of the option."""

    description: str | None = None
    """Description of the option."""

@dataclass
class OnboardingPromptPart(DataModel):
    """Represents fields for creating an onboarding prompt."""

    type: PromptType | None = None
    """Type of prompt."""

    options: list[OnboardingPromptOptionPart] | None = None
    """Options available with the prompt."""

    title: str | None = None
    """Title of the prompt."""

    single_select: bool | None = None
    """Whether the users are limited to selecting one option."""

    required: bool | None = None
    """Whether the prompt is required to complete the onboarding flow."""

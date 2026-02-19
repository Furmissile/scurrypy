from .enum_types import DiscordString, DiscordTypes

class PromptType(DiscordTypes):
    MULTIPLE_CHOICE = 0
    DROPDOWN = 1

class OnboardingMode(DiscordTypes):
    ONBOARDING_DEFAULT = 0
    ONBOARDING_ADVANCED = 1

class StickerType(DiscordTypes):
    """Sticker types."""

    STANDARD = 1
    """An official sticker in a pack."""

    GUILD = 2
    """A sticker uploaded to a guild for the guild's members."""

class StickerFormatType(DiscordTypes):
    PNG = 1
    APNG = 2
    LOTTIE = 3
    GIF = 4

class GuildFeature(DiscordString):
    NEWS = "NEWS"
    ROLE_ICONS = "ROLE_ICONS"
    ANIMATED_ICON = "ANIMATED_ICON"
    INVITE_SPLASH = "INVITE_SPLASH"
    DISCOVERABLE = "DISCOVERABLE"
    BANNER = "BANNER"
    ANIMATED_BANNER = "ANIMATED_BANNER"
    PARTNERED = "PARTNERED"

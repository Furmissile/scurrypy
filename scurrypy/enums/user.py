from .enum_types import DiscordFlags

class GuildMemberFlags(DiscordFlags):
    DID_REJOIN = 1 << 0
    COMPLETED_ONBOARDING = 1 << 1
    BYPASSES_VERIFICATION = 1 << 2
    STARTED_ONBOARDING = 1 << 3
    STARTED_HOME_ACTIONS = 1 << 5
    COMPLETED_HOME_ACTIONS = 1 << 6
    AUTOMOD_QUARANTINED_USERNAME = 1 << 7
    AUTOMOD_QUARANTINED_TAG = 1 << 8

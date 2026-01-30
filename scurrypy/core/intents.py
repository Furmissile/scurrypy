from typing import TypedDict, Unpack

class IntentFlagParams(TypedDict, total=False):
    """Gateway intent selection parameters.
    !!! important
        Param name MUST match the intent it represents! 
        For example, "GUILD_MESSAGES" is "guild_messages".
    """
    guilds: bool
    guild_members: bool
    guild_moderation: bool
    guild_expressions: bool
    guild_integrations: bool
    guild_webhooks: bool
    guild_invites: bool
    guild_messages: bool
    guild_message_reactions: bool
    direct_messages: bool
    direct_message_reactions: bool
    message_content: bool

class Intents:
    """Gateway intent flags (bitwise).  
        For an exhaustive list what intents let your bot listen to what events, 
        see <a href="https://discord.com/developers/docs/events/gateway#list-of-intents" target="_blank" rel="noopener">list of intents</a>.

    !!! note
        Not all intents are listed. Intents not listed are not yet supported.
    """

    GUILDS = 1 << 0
    """Receive events related to guilds."""

    GUILD_MEMBERS = 1 << 1
    """
    !!! warning "Privileged Intent"
        Requires the app setting `Server Members Intent` to be toggled.
    Receive events related to guild members.
    """

    GUILD_MODERATION = 1 << 2
    """Receive events related to guild moderation."""

    GUILD_EXPRESSIONS = 1 << 3
    """Receive events related to custom emojis and stickers."""

    GUILD_INTEGRATIONS = 1 << 4
    """Receive events related to integrations within a guild."""

    GUILD_WEBHOOKS = 1 << 5
    """Receive events related to webhooks."""

    GUILD_INVITES = 1 << 6
    """Receive events related to creating guild invites."""

    GUILD_MESSAGES = 1 << 9
    """Receive events about messages within a guild."""

    GUILD_MESSAGE_REACTIONS = 1 << 10
    """Track changes in reactions on messages."""

    DIRECT_MESSAGES = 1 << 12
    """Receive events related to DMs."""

    DIRECT_MESSAGE_REACTIONS = 1 << 13
    """Receive events related to DM reactions."""

    MESSAGE_CONTENT = 1 << 15
    """
    !!! warning "Privileged Intent"
        Requires the app setting `Message Content Intent` to be toggled.
    Access content of messages.
    """

    DEFAULT = GUILDS | GUILD_MESSAGES

    @staticmethod
    def set(**flags: Unpack[IntentFlagParams]):
        """Set bot intents. See [`Intents`][scurrypy.core.intents.Intents].
        `Intents.DEFAULT` will also be set.

        Args:
            flags (IntentFlagParams): intents to set

        Raises:
            (ValueError): invalid flag

        Returns:
            (int): combined intents field
        """
        intents = Intents.DEFAULT
        for k, v in flags.items():
            if v:
                try:
                    intents |= getattr(Intents, k.upper())
                except AttributeError:
                    raise ValueError(f"Unknown intent flag: '{k}'")
        
        return intents

    @staticmethod
    def has(intents: int, intent: int):
        """Checks if an intent bit is toggled.

        Args:
            intents (int): bot intents
            intent (int): intent bit to check

        Returns:
            (bool): if intent bit is toggled
        """
        return (intents & intent) == intent

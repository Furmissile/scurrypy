from ..events import *

from ..events.event_types import EventTypes

EVENTS = {
    # startup events
    EventTypes.READY: ReadyEvent,

    # channel events
    EventTypes.CHANNEL_CREATE: ChannelCreateEvent,
    EventTypes.CHANNEL_UPDATE: ChannelUpdateEvent,
    EventTypes.CHANNEL_DELETE: ChannelDeleteEvent,
    
    EventTypes.CHANNEL_PINS_UPDATE: ChannelPinsUpdateEvent,

    EventTypes.THREAD_CREATE: ThreadCreateEvent,
    EventTypes.THREAD_UPDATE: ThreadUpdateEvent,
    EventTypes.THREAD_DELETE: ThreadDeleteEvent,

    EventTypes.BULK_MESSAGE_DELETE: BulkMessageDeleteEvent,
    
    EventTypes.WEBHOOKS_UPDATE: WebhooksUpdateEvent,

    # invite events
    EventTypes.INVITE_CREATE: InviteCreateEvent,
    EventTypes.INVITE_DELETE: InviteDeleteEvent,

    # guild events
    EventTypes.GUILD_CREATE: GuildCreateEvent,
    EventTypes.GUILD_UPDATE: GuildUpdateEvent,
    EventTypes.GUILD_DELETE: GuildDeleteEvent,

    EventTypes.GUILD_MEMBER_ADD: GuildMemberAddEvent,
    EventTypes.GUILD_MEMBER_UPDATE: GuildMemberUpdateEvent,
    EventTypes.GUILD_MEMBER_REMOVE: GuildMemberRemoveEvent,

    EventTypes.GUILD_EMOJIS_UPDATE: GuildEmojisUpdateEvent,

    # interaction events
    EventTypes.INTERACTION_CREATE: InteractionEvent,

    # message events
    EventTypes.MESSAGE_CREATE: MessageCreateEvent,
    EventTypes.MESSAGE_UPDATE: MessageUpdateEvent,
    EventTypes.MESSAGE_DELETE: MessageDeleteEvent,

    # reaction events
    EventTypes.MESSAGE_REACTION_ADD: ReactionAddEvent,
    EventTypes.MESSAGE_REACTION_REMOVE: ReactionRemoveEvent,
    EventTypes.MESSAGE_REACTION_REMOVE_ALL: ReactionRemoveAllEvent,
    EventTypes.MESSAGE_REACTION_REMOVE_EMOJI: ReactionRemoveEmojiEvent,

    EventTypes.ROLE_CREATE: RoleCreateEvent,
    EventTypes.ROLE_UPDATE: RoleUpdateEvent,
    EventTypes.ROLE_DELETE: RoleDeleteEvent
}

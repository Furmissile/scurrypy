# scurrypy

import importlib
from typing import TYPE_CHECKING

__all__ = [
    "Logger",
    "Client",
    "Intents",
    "set_intents",
    "BaseConfig",

    "InteractionTypes",  

    "ReadyEvent",

    "ReactionAddEvent",
    "ReactionRemoveEvent",
    "ReactionRemoveEmojiEvent",
    "ReactionRemoveAllEvent",

    "GuildCreateEvent",
    "GuildUpdateEvent",
    "GuildDeleteEvent",

    "MessageCreateEvent",
    "MessageUpdateEvent",
    "MessageDeleteEvent",

    "GuildChannelCreateEvent",
    "GuildChannelUpdateEvent",
    "GuildChannelDeleteEvent",
    "ChannelPinsUpdateEvent",

    "InteractionEvent",

    "ApplicationModel",
    "EmojiModel",
    "GuildModel",
    "MemberModel",
    "UserModel",
    "RoleModel",

    "ChannelTypes",
    "GuildChannel",

    "CommandTypes",
    "CommandOptionTypes",
    "SlashCommand",
    "UserCommand",
    "MessageCommand",

    "ComponentV2Types",
    "SectionPart",
    "TextDisplay",
    "Thumbnail",
    "MediaGalleryItem",
    "MediaGallery",
    "File",
    "SeparatorTypes",
    "Separator",
    "ContainerPart",
    "Label",

    "ComponentTypes",
    "ActionRowPart",
    "ButtonStyles",
    "Button",
    "SelectOption",
    "StringSelect",
    "TextInputStyles",
    "TextInput",
    "DefaultValue",
    "UserSelect",
    "RoleSelect",
    "MentionableSelect",
    "ChannelSelect",

    "EmbedAuthor",
    "EmbedThumbnail",
    "EmbedField",
    "EmbedImage",
    "EmbedFooter",
    "EmbedPart",
    
    "MessageFlags",
    "MessageReferenceTypes",
    "MessageReference",
    "Attachment",
    "MessagePart",

    "ModalPart",
    "Role",

    "ApplicationFlags",
    "Application",

    "BotEmojis",

    "PinnedMessage",
    "Channel",

    "Guild",

    "InteractionCallbackTypes",
    "Interaction",
    
    "Message",
    
    "User",
]

# For editor support / autocomplete
if TYPE_CHECKING:
    from .logger import Logger
    from .client import Client
    from .intents import Intents, set_intents
    from .config import BaseConfig

    from .dispatch.command_dispatcher import InteractionTypes

    # events
    from .events.ready_event import ReadyEvent
    from .events.reaction_events import (
        ReactionAddEvent,
        ReactionRemoveEvent,
        ReactionRemoveEmojiEvent,
        ReactionRemoveAllEvent,
    )
    from .events.guild_events import (
        GuildCreateEvent,
        GuildUpdateEvent,
        GuildDeleteEvent,
    )
    from .events.message_events import (
        MessageCreateEvent,
        MessageUpdateEvent,
        MessageDeleteEvent,
    )
    from .events.channel_events import (
        GuildChannelCreateEvent,
        GuildChannelUpdateEvent,
        GuildChannelDeleteEvent,
        ChannelPinsUpdateEvent,
    )
    from .events.interaction_events import InteractionEvent

    # models
    from .models.application import ApplicationModel
    from .models.emoji import EmojiModel
    from .models.guild import GuildModel
    from .models.member import MemberModel
    from .models.user import UserModel
    from .models.role import RoleModel

    # parts
    from .parts.channel import (
        ChannelTypes, 
        GuildChannel
    )

    from .parts.command import (
        CommandTypes,
        CommandOptionTypes,
        SlashCommand, 
        UserCommand,
        MessageCommand
    )

    from .parts.components_v2 import (
        ComponentV2Types,
        SectionPart,
        TextDisplay,
        Thumbnail,
        MediaGalleryItem,
        MediaGallery,
        File,
        SeparatorTypes,
        Separator,
        ContainerPart,
        Label
    )

    from .parts.components import (
        ComponentTypes,
        ActionRowPart, 
        ButtonStyles,
        Button,
        SelectOption,
        StringSelect,
        TextInputStyles,
        TextInput,
        DefaultValue,
        # SelectMenu,
        UserSelect,
        RoleSelect,
        MentionableSelect,
        ChannelSelect
    )

    from .parts.embed import (
        EmbedAuthor,
        EmbedThumbnail,
        EmbedField,
        EmbedImage,
        EmbedFooter,
        EmbedPart
    )

    from .parts.message import (
        MessageFlags,
        # MessageFlagParams,
        MessageReferenceTypes,
        MessageReference,
        Attachment,
        MessagePart
    )

    from .parts.modal import ModalPart
    from .parts.role import Role

    # resources
    from .resources.application import (
        ApplicationFlags,
        Application
    )

    from .resources.bot_emojis import BotEmojis

    from .resources.channel import (
        # MessagesFetchParams,
        # PinsFetchParams,
        # ThreadFromMessageParams,
        PinnedMessage,
        Channel
    )

    from .resources.guild import (
        # FetchGuildMembersParams,
        # FetchGuildParams,
        Guild
    )

    from .resources.interaction import (
        # InteractionDataTypes,
        InteractionCallbackTypes,
        Interaction
    )

    from .resources.message import Message

    from .resources.user import (
        # FetchUserGuildsParams,
        User
    )

# Lazy loader
def __getattr__(name: str):
    if name not in __all__:
        raise AttributeError(f"module {__name__} has no attribute {name}")

    mapping = {
        # top-level
        "Logger": "scurrypy.logger",
        "Client": "scurrypy.client",
        "Intents": "scurrypy.intents",
        "set_intents": "scurrypy.intents",
        "BaseConfig": "scurrypy.config",

        'InteractionTypes': "scurrypy.dispatch.command_dispatcher",

        "ReadyEvent": "scurrypy.events.ready_event",
        
        "ReactionAddEvent": "scurrypy.events.reaction_events",
        "ReactionRemoveEvent": "scurrypy.events.reaction_events",
        "ReactionRemoveEmojiEvent": "scurrypy.events.reaction_events",
        "ReactionRemoveAllEvent": "scurrypy.events.reaction_events",

        "GuildCreateEvent": "scurrypy.events.guild_events",
        "GuildUpdateEvent": "scurrypy.events.guild_events",
        "GuildDeleteEvent": "scurrypy.events.guild_events",

        "MessageCreateEvent": "scurrypy.events.message_events",
        "MessageUpdateEvent": "scurrypy.events.message_events",
        "MessageDeleteEvent": "scurrypy.events.message_events",

        "GuildChannelCreateEvent": "scurrypy.events.channel_events",
        "GuildChannelUpdateEvent": "scurrypy.events.channel_events",
        "GuildChannelDeleteEvent": "scurrypy.events.channel_events",
        "ChannelPinsUpdateEvent": "scurrypy.events.channel_events",

        "InteractionEvent": "scurrypy.events.interaction_events",

        'ApplicationModel': "scurrypy.models.application",
        'EmojiModel': "scurrypy.models.emoji",
        'GuildModel': "scurrypy.models.guild",
        'MemberModel': "scurrypy.models.member",
        'UserModel': "scurrypy.models.user",
        'RoleModel': "scurrypy.models.role",

        'ChannelTypes': "scurrypy.parts.channel",
        'GuildChannel': "scurrypy.parts.channel",

        'CommandTypes': "scurrypy.parts.command",
        'CommandOptionTypes': "scurrypy.parts.command",
        'SlashCommand': "scurrypy.parts.command",
        'UserCommand': "scurrypy.parts.command",
        'MessageCommand': "scurrypy.parts.command",

        'ComponentV2Types': "scurrypy.parts.components_v2",
        'SectionPart': "scurrypy.parts.components_v2",
        'TextDisplay': "scurrypy.parts.components_v2",
        'Thumbnail': "scurrypy.parts.components_v2",
        'MediaGalleryItem': "scurrypy.parts.components_v2",
        'MediaGallery': "scurrypy.parts.components_v2",
        'File': "scurrypy.parts.components_v2",
        'SeparatorTypes': "scurrypy.parts.components_v2",
        'Separator': "scurrypy.parts.components_v2",
        'ContainerPart': "scurrypy.parts.components_v2",
        'Label': "scurrypy.parts.components_v2",

        'ComponentTypes': "scurrypy.parts.components",
        'ActionRowPart': "scurrypy.parts.components",
        'ButtonStyles': "scurrypy.parts.components",
        'Button': "scurrypy.parts.components",
        'SelectOption': "scurrypy.parts.components",
        'StringSelect': "scurrypy.parts.components",
        'TextInputStyles': 'scurrypy.parts.components',
        'TextInput': "scurrypy.parts.components",
        'DefaultValue': "scurrypy.parts.components",
        'UserSelect': "scurrypy.parts.components",
        'RoleSelect': "scurrypy.parts.components",
        'MentionableSelect': "scurrypy.parts.components",
        'ChannelSelect': "scurrypy.parts.components",
        
        'EmbedAuthor': "scurrypy.parts.embed",
        'EmbedThumbnail': "scurrypy.parts.embed",
        'EmbedField': "scurrypy.parts.embed",
        'EmbedImage': "scurrypy.parts.embed",
        'EmbedFooter': "scurrypy.parts.embed",
        'EmbedPart': "scurrypy.parts.embed",

        'MessageFlags': "scurrypy.parts.message",
        'MessageReferenceTypes': "scurrypy.parts.message",
        'MessageReference': "scurrypy.parts.message",
        'Attachment': "scurrypy.parts.message",
        'MessagePart': "scurrypy.parts.message",

        'ModalPart': "scurrypy.parts.modal",
        'Role': "scurrypy.parts.role",

        'ApplicationFlags': "scurrypy.resources.application",
        'Application': "scurrypy.resources.application",

        'BotEmojis': "scurrypy.resources.bot_emojis",

        'PinnedMessage': "scurrypy.resources.channel",
        'Channel': "scurrypy.resources.channel",

        'Guild': "scurrypy.resources.guild",

        'InteractionCallbackTypes': "scurrypy.resources.interaction",
        'Interaction': "scurrypy.resources.interaction",

        'Message': "scurrypy.resources.message",
        
        'User': "scurrypy.resources.user"
    }

    module = importlib.import_module(mapping[name])
    attr = getattr(module, name)
    globals()[name] = attr  # cache it for future lookups
    return attr

def __dir__():
    return sorted(list(globals().keys()) + __all__)

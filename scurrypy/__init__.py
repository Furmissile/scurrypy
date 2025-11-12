# scurrypy

import importlib
from typing import TYPE_CHECKING

__all__ = [
    # top-level modules
    "Logger", "Client", "Intents", "set_intents", "BaseConfig",

    # events
    "InteractionTypes", "ReadyEvent",
    "ReactionAddEvent", "ReactionRemoveEvent", "ReactionRemoveEmojiEvent", "ReactionRemoveAllEvent",
    "GuildCreateEvent", "GuildUpdateEvent", "GuildDeleteEvent",
    "MessageCreateEvent", "MessageUpdateEvent", "MessageDeleteEvent",
    "GuildChannelCreateEvent", "GuildChannelUpdateEvent", "GuildChannelDeleteEvent", "ChannelPinsUpdateEvent",
    "InteractionEvent",

    # models
    "UserModel", "EmojiModel", "GuildModel", "ApplicationModel", "ReadyGuildModel", "IntegrationModel", 
    "InteractionCallbackDataModel", "InteractionCallbackModel", "MemberModel", "RoleColors", "RoleModel",

    # parts
    "ChannelTypes", "GuildChannel",
    "CommandTypes", "CommandOptionTypes", "SlashCommand", "UserCommand", "MessageCommand",
    "ComponentV2Types", "SectionPart", "TextDisplay", "Thumbnail", "MediaGalleryItem", "MediaGallery",
    "File", "SeparatorTypes", "Separator", "ContainerPart", "Label",
    "ComponentTypes", "ActionRowPart", "ButtonStyles", "Button", "SelectOption", "StringSelect",
    "TextInputStyles", "TextInput", "DefaultValue", "UserSelect", "RoleSelect", "MentionableSelect",
    "ChannelSelect",
    "EmbedAuthor", "EmbedThumbnail", "EmbedField", "EmbedImage", "EmbedFooter", "EmbedPart",
    "MessageFlags", "MessageReferenceTypes", "MessageReference", "Attachment", "MessagePart", "Role", "ModalPart", 

    # resources
    "ApplicationFlags", "Application",
    "BotEmojis",
    "PinnedMessage", "Channel",
    "Guild",
    "InteractionCallbackTypes", "Interaction",
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
    from .models import (
        UserModel,
        EmojiModel,
        GuildModel,
        ApplicationModel,
        ReadyGuildModel,
        IntegrationModel,
        InteractionCallbackDataModel,
        InteractionCallbackModel,
        MemberModel,
        RoleColors,
        RoleModel
    )

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

_lazy_modules = [
    # top-level modules
    (
        "scurrypy.logger",
        [
            "Logger"
        ]
    ),
    (
        "scurrypy.client",
        [
            "Client"
        ]
    ),
    (
        "scurrypy.intents",
        [
            "Intents", 
            "set_intents"
        ]
    ),
    (
        "scurrypy.config",
        [
            "BaseConfig"
        ]
    ),
    (
        "scurrypy.models",
        [
            "UserModel",
            "EmojiModel",
            "GuildModel",
            "ApplicationModel",
            "ReadyGuildModel",
            "IntegrationModel",
            "InteractionCallbackDataModel",
            "InteractionCallbackModel",
            "MemberModel",
            "RoleColors",
            "RoleModel"
        ]
    ),
    
    # Events
    (
        "scurrypy.events.ready_event",
        [
            "ReadyEvent"
        ]
    ),
    (
        "scurrypy.events.reaction_events",
        [
            "ReactionAddEvent", 
            "ReactionRemoveEvent", 
            "ReactionRemoveEmojiEvent", 
            "ReactionRemoveAllEvent"
        ]
    ),
    (
        "scurrypy.events.guild_events",
        [
            "GuildCreateEvent", 
            "GuildUpdateEvent", 
            "GuildDeleteEvent"
        ]
    ),
    (
        "scurrypy.events.message_events",
        [
            "MessageCreateEvent", 
            "MessageUpdateEvent", 
            "MessageDeleteEvent"
        ]
    ),
    (
        "scurrypy.events.channel_events",
        [
            "GuildChannelCreateEvent", 
            "GuildChannelUpdateEvent", 
            "GuildChannelDeleteEvent", 
            "ChannelPinsUpdateEvent"
        ]
    ),
    (
        "scurrypy.events.interaction_events",
        [
            "InteractionEvent"
        ]
    ),

    # Parts
    (
        "scurrypy.parts.channel",
        [
            "ChannelTypes", 
            "GuildChannel"
        ]
    ),
    (
        "scurrypy.parts.command",
        [
            "CommandTypes", 
            "CommandOptionTypes", 
            "SlashCommand", 
            "UserCommand", 
            "MessageCommand"
        ]
    ),
    (
        "scurrypy.parts.components_v2",
        [
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
            "Label"
        ]
    ),
    (
        "scurrypy.parts.components",
        [
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
            "ChannelSelect"
        ]
    ),
    (
        "scurrypy.parts.embed",
        [
            "EmbedAuthor",
            "EmbedThumbnail",
            "EmbedField",
            "EmbedImage",
            "EmbedFooter",
            "EmbedPart"
        ]
    ),
    (
        "scurrypy.parts.message",
        [
            "MessageFlags",
            "MessageReferenceTypes",
            "MessageReference",
            "Attachment",
            "MessagePart"
        ]
    ),
    (
        "scurrypy.parts.modal",
        [
            "ModalPart"
        ]
    ),

    # resources
    (
        "scurrypy.resources.application",
        [
            "ApplicationFlags",
            "Application"
        ]
    ),
    (
        "scurrypy.resources.bot_emojis",
        [
            "BotEmojis"
        ]
    ),
    (
        "scurrypy.resources.channel",
        [
            "PinnedMessage",
            "Channel"
        ]
    ),
    (
        "scurrypy.resources.guild",
        [
            "Guild"
        ]
    ),
    (
        "scurrypy.resources.interaction",
        [
            "InteractionCallbackTypes",
            "Interaction"
        ]
    ),
    (
        "scurrypy.resources.message",
        [
            "Message"
        ]
    ),
    (
        "scurrypy.resources.user",
        [
            "User"
        ]
    )
]

_mapping = {name: module_path 
    for module_path, names in _lazy_modules 
    for name in names
}

def __getattr__(name: str):
    if name not in _mapping:
        raise AttributeError(f"module {__name__} has no attribute {name}")

    module = importlib.import_module(_mapping[name])
    attr = getattr(module, name)
    globals()[name] = attr  # cache it for future lookups
    return attr

def __dir__():
    return sorted(list(globals().keys()) + __all__)

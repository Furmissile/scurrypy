# discord

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
        "Logger": "discord.logger",
        "Client": "discord.client",
        "Intents": "discord.intents",
        "set_intents": "discord.intents",
        "BaseConfig": "discord.config",

        'InteractionTypes': "discord.dispatch.command_dispatcher",

        "ReadyEvent": "discord.events.ready_event",
        
        "ReactionAddEvent": "discord.events.reaction_events",
        "ReactionRemoveEvent": "discord.events.reaction_events",
        "ReactionRemoveEmojiEvent": "discord.events.reaction_events",
        "ReactionRemoveAllEvent": "discord.events.reaction_events",

        "GuildCreateEvent": "discord.events.guild_events",
        "GuildUpdateEvent": "discord.events.guild_events",
        "GuildDeleteEvent": "discord.events.guild_events",

        "MessageCreateEvent": "discord.events.message_events",
        "MessageUpdateEvent": "discord.events.message_events",
        "MessageDeleteEvent": "discord.events.message_events",

        "GuildChannelCreateEvent": "discord.events.channel_events",
        "GuildChannelUpdateEvent": "discord.events.channel_events",
        "GuildChannelDeleteEvent": "discord.events.channel_events",
        "ChannelPinsUpdateEvent": "discord.events.channel_events",

        "InteractionEvent": "discord.events.interaction_events",

        'ApplicationModel': "discord.models.application",
        'EmojiModel': "discord.models.emoji",
        'GuildModel': "discord.models.guild",
        'MemberModel': "discord.models.member",
        'UserModel': "discord.models.user",
        'RoleModel': "discord.models.role",

        'ChannelTypes': "discord.parts.channel",
        'GuildChannel': "discord.parts.channel",

        'CommandTypes': "discord.parts.command",
        'CommandOptionTypes': "discord.parts.command",
        'SlashCommand': "discord.parts.command",
        'UserCommand': "discord.parts.command",
        'MessageCommand': "discord.parts.command",

        'ComponentV2Types': "discord.parts.components_v2",
        'SectionPart': "discord.parts.components_v2",
        'TextDisplay': "discord.parts.components_v2",
        'Thumbnail': "discord.parts.components_v2",
        'MediaGalleryItem': "discord.parts.components_v2",
        'MediaGallery': "discord.parts.components_v2",
        'File': "discord.parts.components_v2",
        'SeparatorTypes': "discord.parts.components_v2",
        'Separator': "discord.parts.components_v2",
        'ContainerPart': "discord.parts.components_v2",
        'Label': "discord.parts.components_v2",

        'ComponentTypes': "discord.parts.components",
        'ActionRowPart': "discord.parts.components",
        'ButtonStyles': "discord.parts.components",
        'Button': "discord.parts.components",
        'SelectOption': "discord.parts.components",
        'StringSelect': "discord.parts.components",
        'TextInputStyles': 'discord.parts.components',
        'TextInput': "discord.parts.components",
        'DefaultValue': "discord.parts.components",
        'UserSelect': "discord.parts.components",
        'RoleSelect': "discord.parts.components",
        'MentionableSelect': "discord.parts.components",
        'ChannelSelect': "discord.parts.components",
        
        'EmbedAuthor': "discord.parts.embed",
        'EmbedThumbnail': "discord.parts.embed",
        'EmbedField': "discord.parts.embed",
        'EmbedImage': "discord.parts.embed",
        'EmbedFooter': "discord.parts.embed",
        'EmbedPart': "discord.parts.embed",

        'MessageFlags': "discord.parts.message",
        'MessageReferenceTypes': "discord.parts.message",
        'MessageReference': "discord.parts.message",
        'Attachment': "discord.parts.message",
        'MessagePart': "discord.parts.message",

        'ModalPart': "discord.parts.modal",
        'Role': "discord.parts.role",

        'ApplicationFlags': "discord.resources.application",
        'Application': "discord.resources.application",

        'BotEmojis': "discord.resources.bot_emojis",

        'PinnedMessage': "discord.resources.channel",
        'Channel': "discord.resources.channel",

        'Guild': "discord.resources.guild",

        'InteractionCallbackTypes': "discord.resources.interaction",
        'Interaction': "discord.resources.interaction",

        'Message': "discord.resources.message",
        
        'User': "discord.resources.user"
    }

    module = importlib.import_module(mapping[name])
    attr = getattr(module, name)
    globals()[name] = attr  # cache it for future lookups
    return attr

def __dir__():
    return sorted(list(globals().keys()) + __all__)

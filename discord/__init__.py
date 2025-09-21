# discord

import importlib
from typing import TYPE_CHECKING

__all__ = [
    # top-level
    "Logger",
    "Client",
    "Intents",
    "set_intents",
    "BaseConfig",

    # events
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

    # models
    "ApplicationModel",
    "EmojiModel",
    "GuildModel",
    "MemberModel",
    "UserModel",
    "RoleModel",

    # parts
    "GuildChannel",
    "Role",
    "MessageBuilder",
    "ModalBuilder",
    "EmbedBuilder",
    "ActionRow",
    "StringSelect",
    "UserSelect",
    "RoleSelect",
    "ChannelSelect",
    "MentionableSelect",
    "SlashCommand",
    "MessageCommand",
    "UserCommand",
    "Container",
    "Section",
    "MediaGalleryItem",
    "Label",

    # resources
    "Guild",
    "Channel",
    "Message",
    "BotEmojis",
    "User",
    "Interaction",
    "Application",
]

# For editor support / autocomplete
if TYPE_CHECKING:
    from .logger import Logger
    from .client import Client
    from .intents import Intents, set_intents
    from .config import BaseConfig

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
    from .parts.channel import GuildChannel
    from .parts.role import Role
    from .parts.message import MessageBuilder
    from .parts.modal import ModalBuilder
    from .parts.embed import EmbedBuilder
    from .parts.action_row import (
        ActionRow, 
        StringSelect,
        UserSelect,
        RoleSelect,
        ChannelSelect,
        MentionableSelect
    )

    from .parts.command import (
        SlashCommand, 
        MessageCommand, 
        UserCommand
    )

    from .parts.components_v2 import (
        Container,
        Section,
        MediaGalleryItem,
        Label
    )

    # resources
    from .resources.guild import Guild
    from .resources.channel import Channel
    from .resources.message import Message
    from .resources.bot_emojis import BotEmojis
    from .resources.user import User
    from .resources.interaction import Interaction
    from .resources.application import Application

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

        # events
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

        # models
        'ApplicationModel': "discord.models.application",
        'EmojiModel': "discord.models.emoji",
        'GuildModel': "discord.models.guild",
        'MemberModel': "discord.models.member",
        'UserModel': "discord.models.user",
        'RoleModel': "discord.models.role",

        # parts
        'GuildChannel': "discord.parts.channel",
        'Role': "discord.parts.role",
        'MessageBuilder': "discord.parts.message",
        'ModalBuilder': "discord.parts.modal",
        'EmbedBuilder': "discord.parts.embed",
        'ActionRow': "discord.parts.action_row",
        'StringSelect': "discord.parts.action_row",
        'UserSelect': "discord.parts.action_row",
        'RoleSelect': "discord.parts.action_row",
        'ChannelSelect': "discord.parts.action_row",
        'MentionableSelect': "discord.parts.action_row",
        'SlashCommand': "discord.parts.command",
        'MessageCommand': "discord.parts.command",
        'UserCommand': "discord.parts.command",
        'Container': "discord.parts.components_v2",
        'Section': "discord.parts.components_v2",
        'MediaGalleryItem': "discord.parts.components_v2",
        'Label': "discord.parts.components_v2",

        # resources
        'Guild': "discord.resources.guild",
        'Channel': "discord.resources.channel",
        'Message': "discord.resources.message",
        'BotEmojis': "discord.resources.bot_emojis",
        'User': "discord.resources.user",
        'Interaction': "discord.resources.interaction",
        'Application': "discord.resources.application"
    }

    module = importlib.import_module(mapping[name])
    attr = getattr(module, name)
    globals()[name] = attr  # cache it for future lookups
    return attr

def __dir__():
    return sorted(list(globals().keys()) + __all__)

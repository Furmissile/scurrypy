from dataclasses import dataclass

from ..core.model import DataModel
from ..core.snowflake import Snowflake

from .base_event import Event

from ..api.channels.channel import ChannelModel
from ..api.guilds.guild import UnavailableGuildModel, GuildModel
from ..api.messages.sticker import StickerModel

from ..api.emoji import EmojiModel
from ..api.user import UserModel, GuildMemberModel

@dataclass
class GuildCreateEvent(Event, GuildModel):
    """Received when the bot has joined a guild."""
    
    joined_at: str
    """ISO8601 timestamp of when app joined the guild."""

    large: bool
    """If the guild is considered large."""

    member_count: int
    """Total number of members in the guild."""

    members: list[GuildMemberModel]
    """Users in the guild."""

    channels: list[ChannelModel]
    """Channels in the guild."""

    threads: list[ChannelModel]
    """All active threads in the guild that are viewable."""

    unavailable: bool | None
    """`True` if the guild is unavailable due to an outage."""

@dataclass
class GuildUpdateEvent(Event, DataModel):
    """Received when a guild has been edited."""

    id: Snowflake
    """ID of the guild."""

    name: str
    """Name of the guild."""

    icon: str
    """Image hash of the guild's icon."""

    description: str
    """Description of the guild."""

    banner: str
    """Image hash of the guild's banner."""

    joined_at: str
    """ISO8601 timestamp of when app joined the guild."""

    large: bool
    """If the guild is considered large."""

    member_count: int
    """Total number of members in the guild."""

@dataclass
class GuildDeleteEvent(Event, UnavailableGuildModel):
    """Received when the bot has left a guild or the guild was deleted."""
    pass

@dataclass
class GuildBanAddEvent(Event, DataModel):
    """Received when a user is banned from a guild."""

    guild_id: Snowflake
    """ID of the guild in which the ban took place."""

    user: UserModel
    """The user who was banned."""

@dataclass
class GuildBanRemoveEvent(Event, DataModel):
    """Received when a user is unbanned from a guild."""

    guild_id: Snowflake
    """ID of the guild in which the ban took place."""

    user: UserModel
    """The user who was banned."""

@dataclass
class GuildEmojisUpdateEvent(Event, DataModel):
    """Received when a guild updates their emojis."""

    guild_id: Snowflake
    """ID of the guild."""

    emojis: list[EmojiModel]
    """Complete set of guild emojis with changes."""

@dataclass
class GuildStickersUpdateEvent(Event, DataModel):
    """Received when a guild's stickers have been updated."""

    guild_id: Snowflake
    """ID of the guild."""

    stickers: list[StickerModel]
    """List of the guild's stickers."""

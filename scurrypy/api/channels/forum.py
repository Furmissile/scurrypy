from dataclasses import dataclass, field

from ...core.model import DataModel
from ...core.snowflake import Snowflake

from ...bases.channel import GuildChannelCreate

from ...enums.channel import ChannelType, SortOrderType, ForumLayoutType

from .channel import ChannelModel
from .default_reaction import DefaultReactionModel, DefaultReactionPart
from .tag import TagModel, TagPart

@dataclass
class GuildForumChannelModel(ChannelModel):
    """Represents the forum channel."""

    available_tags: list[TagModel] | None
    """Set of tags that can be applied to a `GUILD_FORUM` post."""

    applied_tags: list[Snowflake] | None
    """Set of tags applied to a `GUILD_FORUM` post."""

    default_reaction_emoji: DefaultReactionModel | None
    """Emoji to show in the add reaction button in a `GUILD_FORUM` post."""

    default_sort_order: SortOrderType | None
    """Default forum sort order."""

    default_forum_layout: ForumLayoutType | None
    """Default forum layout view. Discord defaults to `ForumLayoutTypes.NOT_SET`."""

@dataclass
class GuildForumChannelPart(DataModel, GuildChannelCreate):
    """Parameters for creating a guild forum channel."""

    name: str | None = None
    """Name of the channel."""

    topic: str | None = None
    """Topic of the channel."""

    position: int | None = None
    """Sorting position of the channel (channels with the same position are sorted by id)."""

    rate_limit_per_user: int | None = None
    """Seconds user must wait between sending messages in the channel."""

    parent_id: Snowflake | None = None
    """Category ID of the channel."""

    nsfw: bool | None = None
    """If the channel is flagged NSFW."""

    default_auto_archive_duration: int | None = None
    """Default duration in minutes threads will be hidden after period of inactivity."""

    default_reaction_emoji: DefaultReactionPart | None = None
    """Emoji to show in the add reaction button in a `GUILD_FORUM` post."""

    available_tags: list[TagPart] | None = None
    """Set of tags that can be applied to a `GUILD_FORUM` post."""

    default_sort_order: SortOrderType | None = None
    """Default forum sort order."""

    default_forum_layout: ForumLayoutType | None = None
    """Default forum layout view."""

    default_thread_rate_limit_per_user: int | None = None
    """Rate limit per user set on newly created threads.
    
    !!! note
        This field does not live update!
    """

    type: ChannelType = field(init=False, default=ChannelType.GUILD_FORUM)
    """Type of channel. Always `ChannelType.GUILD_FORUM` for this class."""

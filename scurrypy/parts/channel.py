from dataclasses import dataclass
from ..core.model import DataModel

from typing import Optional, Literal

class ChannelTypes:
    """Represents the types of channels."""

    GUILD_TEXT = 0
    """Text channel within a guild."""

    GUILD_CATEGORY = 4
    """Organizational category for channels."""

    GUILD_ANNOUNCEMENT = 5
    """Channel users can follow and crosspost into their own server."""

    ANNOUNCEMENT_THREAD = 10
    """Temporary sub-channel within a `GUILD_ANNOUNCEMENT` channel."""

    PUBLIC_THREAD = 11
    """Temporary sub-channel within a `GUILD_TEXT` or `GUILD_FORUM` channel."""

    PRIVATE_THREAD = 12
    """Temporary sub-channel within a `GUILD_TEXT` channel only viewable by invitees and members with `MANAGE_THREADS`."""

    GUILD_DIRECTORY = 14
    """Channel in a hub containing the listed servers."""

    GUILD_FORUM = 15
    """Channel that can only contain threads."""

class ChannelFlags:
    """Represents constant bit fields for channel flags."""

    PINNED = 1 << 1
    """This thread is pinned to the top of its parent `GUILD_FORUM` channel."""

    REQUIRE_TAG = 1 << 4
    """Whether a tag is required when creating a thread in a `GUILD_FORUM` channel."""

class SortOrderTypes:
    """Represents sort order types for `GUILD_FORUM` channels."""

    LATEST_ACTIVITY = 0
    """Sort by activity."""

    CREATION_DATE = 1
    """Sort by creation time (recent to oldest)."""

class ForumLayoutTypes:
    """Represents `GUILD_FORUM` layout types."""

    NOT_SET = 0
    """No default layout has been set."""

    LIST_VIEW = 1
    """Display posts as a list."""

    GALLERY_VIEW = 2
    """Display posts as a collection of tiles."""

@dataclass
class DefaultReactionPart(DataModel):
    """Represents the default reaction for a `GUILD_FORUM` post."""

    emoji_id: int = None
    """ID of the guild's custom emoji."""

    emoji_name: str = None
    """Unicode character of the emoji."""

@dataclass
class TagPart(DataModel):
    """Represents the tag object found in `GUILD_FORUM` channels."""
    
    name: str = None
    """Name of the tag."""

    moderated: bool = None
    """Whether the tag can only be added/removed by a member with `MANAGE_THREADS`."""
    
    emoji_id: int = None
    """ID of a guild's custom emoji."""
    
    emoji_name: str = None
    """Unicode character of the emoji."""

@dataclass
class GuildChannelPart(DataModel):
    """Parameters for creating a guild channel."""

    name: str = None
    """Name of the channel."""

    type: Optional[int] = None
    """Type of channel. See [`ChannelTypes`][scurrypy.parts.channel.ChannelTypes]."""

    topic: Optional[str] = None
    """Topic of the channel."""

    position: Optional[int] = None
    """Sorting position of the channel (channels with the same position are sorted by id)."""

    rate_limit_per_user: Optional[int] = None
    """Seconds user must wait between sending messages in the channel.
    
    !!! note
        Only works for `GUILD_TEXT` and `GUILD_FORUM`.
    """

    parent_id: Optional[int] = None
    """Category ID of the channel.
    
    !!! note
        Only works for `GUILD_TEXT`, `GUILD_ANNOUNCEMENT`, and `GUILD_FORUM`.
    """

    nsfw: Optional[bool] = None
    """If the channel is flagged NSFW.
    
    !!! note
        Only works for `GUILD_TEXT`, `GUILD_ANNOUNCEMENT`, and `GUILD_FORUM`.
    """

    default_auto_archive_duration: Optional[int] = None
    """Default duration in minutes threads will be hidden after period of inactivity.

    !!! note
        Only works for `GUILD_TEXT`, `GUILD_ANNOUNCEMENT`, and `GUILD_FORUM`.
    """

    default_reaction_emoji: Optional[DefaultReactionPart] = None
    """Emoji to show in the add reaction button in a `GUILD_FORUM` post.

    !!! note
        Only works for `GUILD_FORUM`.
    """

    available_tags: Optional[list[TagPart]] = None
    """Set of tags that can be applied to a `GUILD_FORUM` post.
    
    !!! note
        Only works for `GUILD_FORUM`.
    """

    default_sort_order: Optional[int] = None
    """Default forum sort order. See [`SortOrderTypes`][scurrypy.parts.channel.SortOrderTypes].
    
    !!! note
        Only works for `GUILD_FORUM`.
    """

    default_forum_layout: Optional[int] = None
    """Default forum layout view. See [`ForumLayoutTypes`][scurrypy.parts.channel.ForumLayoutTypes].
    
    !!! note
        Only works for `GUILD_FORUM`.
    """

    default_thread_rate_limit_per_user: Optional[int] = None
    """Rate limit per user set on newly created threads.
    
    !!! note
        This field does not live update!

    !!! note
        Only works for `GUILD_TEXT`, `GUILD_ANNOUNCEMENT`, and `GUILD_FORUM`.
    """

@dataclass
class ThreadFromMessagePart(DataModel):
    """Parameters for creating a thread attached to a message."""

    name: str = None
    """Name of the thread."""

    rate_limit_per_user: Optional[int] = None
    """Seconds user must wait between sending messages in the channel."""

    auto_archive_duration: Optional[Literal[60, 1440, 4320, 10080]] = None
    """Duration in minutes threads will be hidden after period of inactivity."""

@dataclass
class ThreadWithoutMessagePart(DataModel):
    """Parameters for creating a thread without a message."""

    name: str = None
    """Name of the thread."""

    rate_limit_per_user: Optional[int] = None
    """Seconds user must wait between sending messages in the channel."""

    auto_archive_duration: Optional[Literal[60, 1440, 4320, 10080]] = None
    """Duration in minutes threads will be hidden after period of inactivity."""

    type: Optional[int] = ChannelTypes.PRIVATE_THREAD
    """Type of thread to create."""

    invitable: Optional[bool] = None
    """Whether non-moderators can add other non-moderators to the thread (private threads only)."""

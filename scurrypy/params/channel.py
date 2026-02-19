from typing import TypedDict, Optional, Literal

from ..enums.channel import ChannelType, ChannelFlags, SortOrderType, ForumLayoutType

from ..api.channels.default_reaction import DefaultReactionPart
from ..api.channels.tag import TagPart

class EditGuildChannelParams(TypedDict, total=False):
    """Parameters for editing a guild channel."""

    name: str
    """Name of the channel."""

    type: Optional[ChannelType]
    """Type of channel.
    
    !!! important
        Only conversion between text and announcement is supported in guilds with `NEWS` feature.
    """

    position: Optional[int]
    """Sorting position of the channel (channels with the same position are sorted by id)."""

    topic: Optional[str]
    """Topic of the channel."""

    nsfw: Optional[bool]
    """If the channel is flagged NSFW."""

    rate_limit_per_user: Optional[int]
    """Seconds user must wait between sending messages in the channel."""

    parent_id: Optional[int]
    """Category ID of the channel."""

    default_auto_archive_duration: Optional[int]
    """Default duration in minutes threads will be hidden after period of inactivity."""

    flags: Optional[ChannelFlags]
    """Channel flags."""

    default_reaction_emoji: Optional[DefaultReactionPart]
    """Emoji to show in the add reaction button in a `GUILD_FORUM` post."""

    available_tags: Optional[list[TagPart]]
    """Set of tags that can be applied to a `GUILD_FORUM` post."""

    default_sort_order: Optional[SortOrderType]
    """Default forum sort order."""

    default_forum_layout: Optional[ForumLayoutType]
    """Default forum layout view."""

    default_thread_rate_limit_per_user: Optional[int]
    """Rate limit per user set on newly created threads.
    
    !!! note
        This field does not live update!
    """

class EditThreadChannelParams(TypedDict, total=False):
    """Parameters for editing a thread channel."""

    name: Optional[str]
    """Name of the channel."""

    archived: Optional[bool]
    """Whether the thread is archived."""

    auto_archive_duration: Optional[Literal[60, 1440, 4320, 10080]]
    """Duration in minutes threads will be hidden after period of inactivity."""

    locked: bool
    """Whether the thread is locked.
    
    !!! note
        Only users with `MANAGE_THREADS` can unarchive the thread.
    """

    invitable: Optional[bool]
    """Whether non-moderators can add other non-moderators to the thread (private threads only)."""

    rate_limit_per_user: Optional[int]
    """Seconds user must wait between sending messages in the channel."""

    flags: Optional[ChannelFlags]
    """Channel flags."""

    applied_tags: Optional[list[int]]
    """Set of tags applied to a `GUILD_FORUM` post."""

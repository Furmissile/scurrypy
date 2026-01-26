from dataclasses import dataclass
from ..core.model import DataModel
from ..core.permissions import Permissions

from typing import Optional

@dataclass
class ThreadMetadataModel(DataModel):
    """Represents the thread metadata object."""

    archived: bool
    """Whether the thread is archived."""

    auto_archive_duration: int
    """How long to wait until the thread is hidden (in minutes)."""

    archive_timestamp: str
    """ISO8601 timestamp of when the thread's archive status was last changed."""

    locked: bool
    """Whether the thread is locked.
    
    !!! note
        Only users with `MANAGE_THREADS` can unarchive the thread.
    """

    invitable: Optional[bool]
    """Whether non-moderators can add other non-moderators to the thread (private threads only)."""

    create_timestamp: Optional[str]
    """ISO8601 timestamp of thread creation (field only exists after Jan 09, 2022)."""

from .user import GuildMemberModel

@dataclass
class ThreadMemberModel(DataModel):
    """Represents a user that has joined a thread."""

    id: Optional[int]
    """ID of the thread."""

    user_id: Optional[int]
    """ID of the user."""

    join_timestamp: str
    """ISO8601 timestamp of when the user last joined the thread."""

    member: Optional[GuildMemberModel]
    """Additional information about the user.
    
    !!! note
        Only present when `with_member` is toggled on request.
    """

@dataclass
class TagModel(DataModel):
    """Represents the tag object found in `GUILD_FORUM` channels."""
    
    id: int
    """ID of the tag."""

    name: str
    """Name of the tag."""

    moderated: bool
    """Whether the tag can only be added/removed by a member with `MANAGE_THREADS`."""
    
    emoji_id: int
    """ID of a guild's custom emoji."""
    
    emoji_name: str
    """Unicode character of the emoji."""

@dataclass
class DefaultReactionModel(DataModel):
    """Represents the default reaction for a `GUILD_FORUM` post."""

    emoji_id: int
    """ID of the guild's custom emoji."""

    emoji_name: str
    """Unicode character of the emoji."""

from .user import UserModel

@dataclass
class ChannelModel(DataModel):
    """Represents a Discord guild channel."""

    id: int
    """ID of the channel."""

    type: int
    """Type of channel."""

    guild_id: Optional[int]
    """Guild ID of the channel."""

    parent_id: Optional[int]
    """Category ID of the channel."""

    position: Optional[int]
    """Position of the channel."""

    name: Optional[str]
    """Name of the channel."""

    topic: Optional[str]
    """Topic of the channel."""

    nsfw: Optional[bool]
    """If the channel is flagged NSFW."""

    last_message_id: Optional[int]
    """ID of the last message sent in the channel."""

    rate_limit_per_user: Optional[int]
    """Seconds user must wait between sending messages in the channel."""

    recipients: Optional[list[UserModel]]
    """Recipients of the DM."""

    icon: Optional[str]
    """Icon hash of the group DM."""

    owner_id: Optional[int]
    """ID of the creator of the group DM or thread."""

    application_id: Optional[int]
    """ID of the application that created the DM or thread."""

    last_pin_timestamp: Optional[str]
    """ISO8601 timestamp of the last pinned messsage in the channel."""

    permissions: Optional[int]
    """Permissions for the invoking user in this channel.
        Includes role and overwrite calculations. [`INT_LIMIT`]
    """

    thread_metadata: Optional[ThreadMetadataModel]
    """Thread-specific fields not needed by other channels."""

    member: Optional[ThreadMemberModel]
    """Thread member object for the current user if they have joined the thread."""

    default_auto_archive_duration: Optional[int]
    """Default duration in minutes threads will be hidden after period of inactivity."""

    flags: Optional[int]
    """Channel flags combined as a bitfield. See [`ChannelFlags`][scurrypy.parts.channel.ChannelFlags]."""

    available_tags: Optional[list[TagModel]]
    """Set of tags that can be applied to a `GUILD_FORUM` post."""

    applied_tags: Optional[list[int]]
    """Set of tags applied to a `GUILD_FORUM` post."""

    default_reaction_emoji: Optional[DefaultReactionModel]
    """Emoji to show in the add reaction button in a `GUILD_FORUM` post."""

    default_thread_rate_limit_per_user: Optional[int]
    """Rate limit per user set on newly created threads.
    
    !!! note
        This field does not live update!
    """

    default_sort_order: Optional[int]
    """Default forum sort order. See [`SortOrderTypes`][scurrypy.parts.channel.SortOrderTypes]."""

    default_forum_layout: Optional[int]
    """Default forum layout view. Defaults to `ForumLayoutTypes.NOT_SET`. See [`ForumLayoutTypes`][scurrypy.parts.channel.ForumLayoutTypes]."""

    def user_can(self, permission_bit: int):
        """Checks `permissions` to see if permission bit is toggled.

        !!! warning
            If `permission` field is `None`, this function always returns `False`.

        Args:
            permission_bit (int): permission bit. See [`Permissions`][scurrypy.core.permissions.Permissions].

        Returns:
            (bool): whether the user has this permission
        """
        if not self.permissions:
            return False
        return Permissions.has(self.permissions, permission_bit)

@dataclass
class FollowedChannelModel(DataModel):
    """Represents the followed channel object."""

    channel_id: int
    """ID of the source channel."""

    webhook_id: int
    """Target webhook ID created."""

@dataclass
class ArchivedThreadsModel(DataModel):
    """Response body for fetching archived threads."""

    threads: list[ChannelModel]
    """The archived threads."""

    members: list[ThreadMemberModel]
    """Thread member for each returned thread the bot has joined."""

    has_more: bool
    """Whether there are additional threads to be returned with subsequent calls."""

@dataclass
class ActiveThreadsModel(DataModel):
    """Response body for fetching active guild threads."""

    threads: list[ChannelModel]
    """The arctive threads."""

    members: list[ThreadMemberModel]
    """Thread member for each returned thread the bot has joined."""

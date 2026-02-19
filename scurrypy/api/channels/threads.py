from dataclasses import dataclass

from ...core.model import DataModel
from ...core.snowflake import Snowflake

from ...enums.channel import ChannelType, AutoArchiveDurationType

from ..user import GuildMemberModel

from .channel import ChannelModel

@dataclass
class ThreadFromMessagePart(DataModel):
    """Parameters for creating a thread attached to a message."""

    name: str = None
    """Name of the thread."""

    rate_limit_per_user: int | None = None
    """Seconds user must wait between sending messages in the channel."""

    auto_archive_duration: AutoArchiveDurationType | None = None
    """Duration in minutes threads will be hidden after period of inactivity."""

@dataclass
class ThreadWithoutMessagePart(DataModel):
    """Parameters for creating a thread without a message."""

    name: str = None
    """Name of the thread."""

    rate_limit_per_user: int | None = None
    """Seconds user must wait between sending messages in the channel."""

    auto_archive_duration: AutoArchiveDurationType | None = None
    """Duration in minutes threads will be hidden after period of inactivity."""

    type: ChannelType | None = None
    """Type of thread to create. If omitted, Discord defaults to `ChannelType.PRIVATE_THREAD`."""

    invitable: bool | None = None
    """Whether non-moderators can add other non-moderators to the thread (private threads only)."""

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

    invitable: bool | None
    """Whether non-moderators can add other non-moderators to the thread (private threads only)."""

    create_timestamp: str | None
    """ISO8601 timestamp of thread creation (field only exists after Jan 09, 2022)."""

@dataclass
class ThreadMemberModel(DataModel):
    """Represents a user that has joined a thread."""

    id: Snowflake | None
    """ID of the thread."""

    user_id: Snowflake | None
    """ID of the user."""

    join_timestamp: str
    """ISO8601 timestamp of when the user last joined the thread."""

    member: GuildMemberModel | None
    """Additional information about the user.
    
    !!! note
        Only present when `with_member` is toggled on request.
    """

    default_thread_rate_limit_per_user: int | None
    """Rate limit per user set on newly created threads.
    
    !!! note
        This field does not live update!
    """

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

@dataclass
class ThreadChannelModel(ChannelModel):
    """Represents the thread channel."""

    owner_id: Snowflake | None
    """ID of the creator of the thread."""

    application_id: Snowflake | None
    """ID of the application that created thread."""

    thread_metadata: ThreadMetadataModel | None
    """Thread-specific fields not needed by other channels."""

    member: ThreadMemberModel | None
    """Thread member object for the current user if they have joined the thread."""

    default_auto_archive_duration: int | None
    """Default duration in minutes threads will be hidden after period of inactivity."""

from dataclasses import dataclass, field

from ...core.model import DataModel
from ...core.snowflake import Snowflake

from ...bases.channel import GuildChannelCreate

from ...enums.channel import ChannelType

@dataclass
class GuildTextChannelPart(DataModel, GuildChannelCreate):
    """Parameters for creating a guild text channel."""

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

    default_thread_rate_limit_per_user: int | None = None
    """Rate limit per user set on newly created threads.
    
    !!! note
        This field does not live update!
    """

    type: ChannelType = field(init=False, default=ChannelType.GUILD_TEXT)
    """Type of channel. Always `ChannelType.GUILD_TEXT` for this class."""

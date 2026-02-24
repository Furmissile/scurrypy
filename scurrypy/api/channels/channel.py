from dataclasses import dataclass

from ...core.model import DataModel
from ...core.snowflake import Snowflake

from ...enums.permissions import Permissions
from ...enums.channel import ChannelFlags

@dataclass
class ChannelModel(DataModel):
    """Represents common channel fields."""

    id: Snowflake
    """ID of the channel."""

    flags: ChannelFlags
    """Channel flags combined as a bitfield."""

    guild_id: Snowflake | None
    """Guild ID of the channel."""

    parent_id: Snowflake | None
    """Category ID of the channel."""

    position: int | None
    """Position of the channel."""

    name: str | None
    """Name of the channel."""

    topic: str | None
    """Topic of the channel."""

    nsfw: bool | None
    """If the channel is flagged NSFW."""

    last_message_id: Snowflake | None
    """ID of the last message sent in the channel."""

    rate_limit_per_user: int | None
    """Seconds user must wait between sending messages in the channel."""

    last_pin_timestamp: str | None
    """ISO8601 timestamp of the last pinned messsage in the channel."""

    permissions: Permissions | None
    """Permissions for the invoking user in this channel.
        Includes role and overwrite calculations. [`INT_LIMIT`]
    """

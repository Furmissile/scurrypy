from dataclasses import dataclass

from ...core.model import DataModel
from ...core.snowflake import Snowflake

@dataclass
class FollowedChannelModel(DataModel):
    """Represents the followed channel object."""

    channel_id: Snowflake
    """ID of the source channel."""

    webhook_id: Snowflake
    """Target webhook ID created."""

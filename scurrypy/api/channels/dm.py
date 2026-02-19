from dataclasses import dataclass

from ...core.snowflake import Snowflake

from ..user import UserModel

from .channel import ChannelModel

@dataclass
class DMChannelModel(ChannelModel):
    """Represents a DM channel."""

    recipients: list[UserModel] | None
    """Recipients of the DM."""

    icon: str | None
    """Icon hash of the group DM."""

    owner_id: Snowflake | None
    """ID of the creator of the group DM."""

    application_id: Snowflake | None
    """ID of the application that created the DM."""

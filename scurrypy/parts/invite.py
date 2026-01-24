from dataclasses import dataclass, field
from ..core.model import DataModel

from typing import Optional

@dataclass
class InvitePart(DataModel):
    """Represents fields for creating an invite."""

    max_age: int = 86400
    """Duration of invite (in seconds) before it expires. 
    `0` for never or up to `604800` (max 7 days).
    Defaults to `86400` (24 hours).
    """

    max_uses: int = 0
    """Max number of uses for this invite.
    `0` for unlimited or up to `100`.
    Defaults to `0`.
    """

    temporary: bool = False
    """Whether this invite grants temporary membership.
    Defaults to `False`.
    """

    unique: bool = False
    """Whether to reuse similar invite codes.
    Defaults to `False`.
    """

    role_ids: Optional[list[int]] = field(default_factory=list)
    """Role IDs to be given when the user accept this invite.
    
    !!! important "Permissions"
        Requires `MANAGE_ROLES` and cannot assign roles with higher
        permissions than the sender.
    """

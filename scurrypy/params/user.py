from typing import TypedDict

from ..parts.image_data import ImageDataPart

class EditGuildMemberParams(TypedDict, total=False):
    """Parameters for editing a guild member."""

    nick: str
    """User's guild nickname.
    
    !!! important "Permissions"
        Requires `MANAGE_NICKNAMES`
    """

    roles: list[int]
    """Role IDs the member is assigned.
    
    !!! important "Permissions"
        Requires `MANAGE_ROLES`
    """

class EditUserParams(TypedDict, total=False):
    """Parameters for editing a user."""

    username: str
    """User's username.
    
    !!! note
        May cause the discriminator to be randomized.
    """

    avatar: ImageDataPart
    """User's avatar."""

    banner: ImageDataPart
    """User's banner."""

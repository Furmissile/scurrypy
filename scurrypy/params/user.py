from typing import TypedDict

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

from typing import TypedDict

class EditGuildEmojiParams(TypedDict, total=False):
    """Parameters for editing a guild emoji."""

    name: str
    """Name of the moji."""

    roles: list[int]
    """Roles allowed to use this emoji."""

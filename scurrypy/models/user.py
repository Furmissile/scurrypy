from dataclasses import dataclass

from ..model import DataModel

@dataclass
class UserModel(DataModel):
    """Describes the User object."""
    id: int
    """ID of the user."""

    username: str
    """Username of the user."""

    avatar: str
    """Avatar hash of the user."""

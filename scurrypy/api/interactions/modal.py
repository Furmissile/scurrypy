from dataclasses import dataclass

from ...core.model import DataModel

from ..components.layout import Label

@dataclass
class ModalPart(DataModel):
    """Represents the Modal object."""

    title: str | None = None
    """Title of the popup modal."""

    custom_id: str | None = None
    """ID for the modal."""

    components: list[Label] | None = None
    """1 to 5 components that make up the modal."""

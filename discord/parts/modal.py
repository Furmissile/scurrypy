from dataclasses import dataclass, field
from discord.model import DataModel
from .components_v2 import Label

@dataclass
class ModalBuilder(DataModel):
    title: str
    custom_id: str = None
    components: list[Label] = field(default_factory=list)

    def add_label(self, component: Label):
        """Add a label component to this modal.

        Args:
            component (Label): the label component

        Returns:
            ModalBuilder: self
        """
        self.components.append(component)
        return self

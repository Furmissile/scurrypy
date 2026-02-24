from dataclasses import dataclass, field

from ...bases.components import (
    Component,
    ActionRowChild, 
    SectionAccessoryChild
)

from ...enums.components import (
    ComponentType,
    ButtonStyle
)

from ..emoji import EmojiModel

@dataclass
class Button(Component, ActionRowChild, SectionAccessoryChild):
    """Represents the Button component.
    
    A pressable button!
    """

    style: ButtonStyle | None = None
    """A button style."""

    custom_id: str | None = None
    """ID for the button. Do not supply for `ButtonStyles.LINK` style buttons."""

    label: str | None = None
    """Text that appears on the button."""

    emoji: EmojiModel | None = None
    """Emoji icon for the button."""

    url: str | None = None
    """URL for link-style buttons."""

    disabled: bool | None = None
    """Whether the button is disabled. Discord defaults to `False`."""

    link: str | None = None
    """Hyperlink for button. For `ButtonStyles.LINK` style only."""

    type: ComponentType = field(init=False, default=ComponentType.BUTTON)
    """Component type. Always `ComponentType.BUTTON` for this class."""

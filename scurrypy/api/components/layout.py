from dataclasses import dataclass, field

from ...core.model import DataModel

from ...bases.components import (
    ContainerChild, 
    SectionAccessoryChild,
    SectionChild,
    Component
)

from ...enums.components import (
    ComponentType,
    SeparatorType
)

@dataclass
class ActionRow(Component):
    """Represents a container of interactable components."""

    components: list[Component] | None = None
    """Up to 5 interactive button components or a single select component."""

    type: ComponentType = field(init=False, default=ComponentType.ACTION_ROW)
    """Component type."""

@dataclass
class Section(Component, ContainerChild):
    """Represents the Section component.
    
    A Section contextually associates content with an accessory component.
    """

    accessory: Component | None = None
    """A component that is contextually associated to the content of the section.
    
    Supports [`SectionAccessoryChild`][scurrypy.bases.components.SectionAccessoryChild] components.
    """

    components: list[Component] | None = None
    """Component(s) representing the content of the section that is contextually associated to the accessory.
    
    Supports [`SectionChild`][scurrypy.bases.components.SectionChild] components.
    """

    type: ComponentType = field(init=False, default=ComponentType.SECTION)
    """Component type. Always `ComponentType.SECTION` for this class."""


@dataclass
class TextDisplay(Component, ContainerChild, SectionChild):
    """Represents the Text Display component.
    
    A Text Display adds markdown formatted text, including mentions (users, roles, etc) and emojis.
    """

    content: str | None = None
    """Text that will be displayed similar to a message."""

    type: ComponentType = field(init=False, default=ComponentType.TEXT_DISPLAY)
    """Component type. Always `ComponentType.TEXT_DISPLAY` for this class."""

@dataclass
class Thumbnail(Component, SectionAccessoryChild):
    """Represents the Thumbnail component.
    
    A Thumbnail displays visual media in a small form-factor.
    """
    
    media: str | None = None
    """Media of the thumbnail. http or attachment://<filename> scheme."""

    description: str | None = None
    """Description for the media."""

    spoiler: bool | None = None
    """Whether the thumbnail should be a spoiler (or blurred out). Discord defaults to `False`."""

    type: ComponentType = field(init=False, default=ComponentType.THUMBNAIL)
    """Component type. Always `ComponentType.THUMBNAIL` for this class."""

@dataclass
class MediaGalleryItem(DataModel):
    """Represents the Media Gallery Item component."""

    media: str | None = None
    """Image data. http or attachment://<filename> scheme."""

    description: str | None = None
    """Alt text for the media."""

    spoiler: bool | None = None
    """Whether the thumbnail should be a spoiler (or blurred out). Discord defaults to `False`."""

@dataclass
class MediaGallery(Component, ContainerChild):
    """Represents the Media Gallery component.
    
    A Media Gallery displays 1-10 media attachments in an organized gallery format.
    """

    items: list[MediaGalleryItem] | None = None
    """1 to 10 nedia gallery items."""

    type: ComponentType = field(init=False, default=ComponentType.MEDIA_GALLERY)
    """Component type. Always `ComponentType.MEDIA_GALLERY` for this class."""

@dataclass
class File(Component, ContainerChild):
    """Represents the File component.
    
    A File displays an uploaded file as an attachment to the message and reference it in the component.
    """

    file: str | None = None
    """File name. ONLY supports attachment://<filename> scheme."""

    spoiler: bool | None = None
    """Whether the thumbnail should be a spoiler (or blurred out). Discord defaults to `False`."""

    type: ComponentType = field(init=False, default=ComponentType.FILE)
    """Component type. Always `ComponentType.FILE` for this class."""

@dataclass
class Separator(Component, ContainerChild):
    """Represents the Separator component.
    
    A Separator adds vertical padding and visual division between other components.
    """

    divider: bool | None = None
    """Whether a visual divider should be displayed in the component. Discord defaults to `True`."""

    spacing: SeparatorType | None = None
    """Size of separator padding. Discord defaults to `SeparatorType.SMALL_PADDING`."""

    type: ComponentType = field(init=False, default=ComponentType.SEPARATOR)
    """Component type. Always `ComponentType.SEPARATOR` for this class."""

@dataclass
class Container(Component):
    """Represents a container of display and interactable components.
    
    A Container visually encapsulates a collection of components.
    """

    components: list[Component] | None = None
    """Child components that are encapsulated within the Container. 
    
    Supports [`ContainerChild`][scurrypy.bases.components.ContainerChild] components.
    """

    accent_color: int | None = None
    """Color for the accent as an integer."""

    spoiler: bool | None = None
    """If the container should be blurred out. Discord defaults to `False`."""

    type: ComponentType = field(init=False, default=ComponentType.CONTAINER)
    """Component type. Always `ComponentType.CONTAINER` for this class."""

@dataclass
class Label(Component):
    """Represents the Discord Label component.
    
    Labels wrap modal components with text as a label and optional description.
    """

    label: str | None = None
    """Label text."""

    component: Component | None = None
    """A component within the label. 
    
    Supports [`LabelChild`][scurrypy.bases.components.LabelChild] components.
    """

    description: str | None = None
    """An optional description text for the label."""

    type: ComponentType = field(init=False, default=ComponentType.LABEL)
    """Component type. Always `ComponentType.LABEL` for this class."""

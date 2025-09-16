from dataclasses import dataclass, field
from typing import Literal, Optional
from ..model import DataModel

from .component_types import *
from .action_row import StringSelect, ActionRow

class _TextInputStyles:
    """Represents the types of Text Inputs."""
    SHORT = 1 # one line
    PARAGRAPH = 2 # multiple lines

@dataclass
class _TextInput(DataModel, LabelChild):
    """Represents the Text Input component."""
    type: Literal[4] = field(init=False, default=4)
    style: _TextInputStyles = _TextInputStyles.SHORT # refer to _TextInputStyles for details
    custom_id: str = None
    required: Optional[bool] = False
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    value: Optional[str] = None
    placeholder: Optional[str] = None

@dataclass
class Section(DataModel, ContainerChild):
    """Represents the Section component."""
    type: Literal[9] = field(init=False, default=9)
    accessory: Optional[SectionAccessory] = None
    components: list[SectionChild] = field(default_factory=list)

@dataclass
class _TextDisplay(DataModel, ContainerChild, SectionChild):
    """Represents the Text Display component."""
    type: Literal[10] = field(init=False, default=10)
    content: str


@dataclass
class _Thumbnail(DataModel, SectionAccessory):
    """Represents the _Thumbnail component."""
    type: Literal[11] = field(init=False, default=11)
    media: str  # http or attachment://<filename>
    description: Optional[str] = None
    spoiler: Optional[bool] = False


@dataclass
class MediaGalleryItem(DataModel):
    """Represents the Media Gallery Item component."""

    media: str
    """Image data. http or attachment://<filename> scheme."""

    description: Optional[str] = None
    """Alt text for the media."""

    spoiler: Optional[bool] = False
    """If the media should be blurred out."""

@dataclass
class _MediaGallery(DataModel, ContainerChild):
    """Represents the Media Gallery component."""
    type: Literal[12] = field(init=False, default=12)
    items: list[MediaGalleryItem] = field(default_factory=list)


@dataclass
class _File(DataModel, ContainerChild):
    """Represents the File component."""
    type: Literal[13] = field(init=False, default=13)
    file: str # http or attachment://<filename>
    spoiler: Optional[bool] = False

class _SeparatorTypes:
    """Represents separator types constants."""
    SMALL_PADDING = 1
    LARGE_PADDING = 2

@dataclass
class _Separator(DataModel, ContainerChild):
    """Represents the Separator component."""
    type: Literal[14] = field(init=False, default=14)
    divider: bool = True
    spacing: Optional[int] = _SeparatorTypes.SMALL_PADDING # refer to _SeparatorTypes

@dataclass
class Label(DataModel):
    """Represents the Discord Label component."""
    label: str
    """Label text."""

    component: LabelChild = None
    """A component within the label."""

    description: Optional[str] = None
    """An optional description text for the label."""

    type: Literal[18] = field(init=False, default=18)

    def string_select(self, select: StringSelect):
        """Set this label to be a string select component.

        Args:
            select (StringSelect): the string select component

        Returns:
            (Label): self
        """
        self.component = select
        return self

    def text_input(self,
        *,
        custom_id: str,
        min_length: int,
        max_length: int,
        value: str = None,
        style: Literal['Short', 'Paragraph'] = 'Short',
        placeholder: str = None,
        require: bool = False
    ):
        """Set this label to be a text input component.

        Args:
            custom_id (str): developer-defined component ID
            min_length (int): minimum number of characters required
            max_length (int): maximum number of characters required
            value (str, optional): component value
            style (Literal['Short', 'Paragraph'], optional): 
                text format. Defaults to 'Short'.
            placeholder (str, optional): custom placeholder text if empty
            require (bool, optional): if input is required. Defaults to False.

        Returns:
            (Label): self
        """
        _styles = {
            'SHORT': _TextInputStyles.SHORT,
            'PARAGRAPH': _TextInputStyles.PARAGRAPH
        }

        self.component = _TextInput(
            style = _styles.get(style.upper()),
            placeholder=placeholder,
            custom_id=custom_id,
            min_length=min_length,
            max_length=max_length,
            value=value,
            required=require
        )
        return self

@dataclass
class Container(DataModel):
    """Represents a container of display and interactable components."""
    type: Literal[17] = field(init=False, default=17)

    components: list[ContainerChild] = field(default_factory=list)
    """Child components that are encapsulated within the Container."""

    accent_color: Optional[int] = None
    """Color for the accent as an integer."""

    spoiler: Optional[bool] = False
    """If the container should be blurred out."""

    def set_color(self, hex: str):
        """Set this container's color with a hex. (format: #FFFFFF)

        Args:
            hex (str): color as a hex code

        Returns:
            (Container): self
        """
        self.accent_color = int(hex.strip('#'), 16)
        return self

    def add_row(self, row: ActionRow):
        """Add an action row to this container.

        Args:
            row (ActionRow): the ActionRow object
        
        Returns:
            (Container): self
        """
        self.components.append(row)
        return self
    
    def add_section(self, section: Section):
        """Add a section to this container.

        Args:
            section (Section): the Section object
        
        Returns:
            (Container): self
        """
        self.components.append(section)
        return self
    
    def add_text_display(self, content: str):
        """Add a text display to this container.

        Args:
            content (str): the content to display
        
        Returns:
            (Container): self
        """
        self.components.append(_TextDisplay(content))
        return self
    
    def set_thumbnail(self, media: str, description: str = None, has_spoiler: bool = False):
        """Set the thumbnail for this container

        Args:
            media (str): Image data. http or attachment://<filename> scheme.
            description (str, optional): Alt text for the media
            has_spoiler (bool, optional): If the media should be blurred out. Defaults to False.

        Returns:
            (Container): self
        """
        self.components.append(_Thumbnail(media, description, has_spoiler))
        return self
    
    def set_media_gallery(self, items: list[MediaGalleryItem]):
        """Add a media gallery to this container.

        Args:
            items (list[MediaGalleryItem]): list of media gallery images

        Returns:
            (Container): self
        """
        self.components.append(_MediaGallery(items))
        return self
    
    def add_attachment(self, file: str, has_spoiler: bool = False):
        """Add a single attachment to this container.

        Args:
            file (str): Image data. http or attachment://<filename> scheme
            has_spoiler (bool, optional): If the media should be blurred out. Defaults to False.

        Returns:
            (Container): self
        """
        self.components.append(_File(file, has_spoiler))
        return self
    
    def add_separator(self, spacing: Literal['Small', 'Large'] = 'Small', has_divider: bool = True):
        """Add a separator to this container. Positionally accurate.

        Args:
            spacing (Literal['Small', 'Large'], optional): size of separator padding. Defaults to 'Small'.
            has_divider (bool, optional): if a visual divider should be shown. Defaults to True.

        Returns:
            (Container): self
        """
        _spacing_types = {
            'SMALL': _SeparatorTypes.SMALL_PADDING,
            'LARGE': _SeparatorTypes.LARGE_PADDING
        }
        self.components.append(_Separator(divider=has_divider, spacing=_spacing_types.get(spacing.upper())))
        return self

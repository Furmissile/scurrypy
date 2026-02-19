from dataclasses import dataclass, field

from ...core.model import DataModel

from ...bases.components import (
    LabelChild,
    Component
)

from ...enums.components import (
    ComponentType,
    TextInputStyle
)

@dataclass
class TextInput(DataModel, Component, LabelChild):
    """Represents the Text Input component.
    
    A Text Input allows users to enter free-form text.
    """

    custom_id: str | None = None
    """ID for the input."""

    style: TextInputStyle | None = None
    """Text input style. Discord defaults to `TextInputStyle.SHORT`."""

    min_length: int | None = None
    """Minimum input length for a text input."""

    max_length: int | None = None
    """Maximum input length for a text input."""

    required: bool | None = None
    """Whether this component is required to be filled. Discord defaults to `True`."""

    value: str | None = None
    """Pre-filled value for this component."""

    placeholder: str | None = None
    """Custom placeholder text if the input is empty."""

    type: ComponentType = field(init=False, default=ComponentType.TEXT_INPUT)
    """Component type. Always `ComponentType.TEXT_INPUT` for this class."""


@dataclass
class FileUpload(DataModel, Component, LabelChild):
    """Represents the file upload component.
    
    File Upload allows users to upload files in modals.
    """

    custom_id: str | None = None
    """ID for the file upload."""

    min_values: int | None = None
    """Minimum number of items that must be uploaded. Discord defaults to `1`."""

    max_values: int | None = None
    """Maximum number of items that can be uploaded. Discord defaults to `1`."""

    required: bool | None = None
    """Whether files are required to be uploaded. Discord defaults to `True`."""

    type: ComponentType = field(init=False, default=ComponentType.FILE_UPLOAD)
    """Component type. Always `ComponentType.FILE_UPLOAD` for this class."""

@dataclass
class ListOption(DataModel):
    """Represents an option in a group or checkbox group component."""

    value: str | None = None
    """ID for the option."""

    label: str | None = None
    """User-facing label for the option."""

    description: str | None = None
    """Description for the option."""

    default: bool | None = None
    """Whether to show this option as selected by default."""

@dataclass
class RadioGroup(DataModel, Component, LabelChild):
    """Represents the radio group component.
    
    A Radio Group is for selecting exactly one option from a defined list.
    """

    custom_id: str | None = None
    """ID for the radio group."""

    options: list[ListOption] | None = None
    """List of options to show."""

    required: bool | None = None
    """Whether a selection is required for submission. Discord defaults to `True`."""

    type: ComponentType = field(init=False, default=ComponentType.RADIO_GROUP)
    """Component type. Always `ComponentType.RADIO_GROUP` for this class."""

@dataclass
class CheckboxGroup(DataModel, Component, LabelChild):
    """Represents the checkbox group component.
    
    A Checkbox Group is for selecting one or many options via checkboxes.
    """

    custom_id: str | None = None
    """ID for the checkbox group."""

    options: list[ListOption] | None = None
    """List of options to show."""

    min_values: int | None = None
    """Minimum number of items that must be chosen. Discord defaults to `1`."""

    max_values: int | None = None
    """Maximum number of items that must be chosen. Discord defaults to `1`."""

    required: bool | None = None
    """Whether a selection is required for submission. Discord defaults to the number of options."""

    type: ComponentType = field(init=False, default=ComponentType.CHECKBOX_GROUP)
    """Component type. Always `ComponentType.CHECKBOX_GROUP` for this class."""

@dataclass
class Checkbox(DataModel, Component, LabelChild):
    """Represents a checkbox component.
    
    A Checkbox is for simple yes/no style questions.
    """

    custom_id: str | None = None
    """ID for the option."""

    default: bool | None = None
    """Whether to show this option as selected by default."""

    type: ComponentType = field(init=False, default=ComponentType.CHECKBOX)
    """Component type. Always `ComponentType.CHECKBOX` for this class."""

from ...enums.components import ComponentType

from .button import Button
from .layout import ActionRow, Section, TextDisplay, Thumbnail, MediaGallery, File, Separator, Container, Label
from .modal import TextInput, FileUpload, RadioGroup, CheckboxGroup, Checkbox
from .select_menu import StringSelect, UserSelect, RoleSelect, MentionableSelect, ChannelSelect

COMPONENT_MAP = {
    ComponentType.ACTION_ROW: ActionRow,
    ComponentType.BUTTON: Button,
    ComponentType.STRING_SELECT: StringSelect,
    ComponentType.TEXT_INPUT: TextInput,
    ComponentType.USER_SELECT: UserSelect,
    ComponentType.ROLE_SELECT: RoleSelect,
    ComponentType.MENTIONABLE_SELECT: MentionableSelect,
    ComponentType.CHANNEL_SELECT: ChannelSelect,
    ComponentType.SECTION: Section,
    ComponentType.TEXT_DISPLAY: TextDisplay,
    ComponentType.THUMBNAIL: Thumbnail,
    ComponentType.MEDIA_GALLERY: MediaGallery,
    ComponentType.FILE: File,
    ComponentType.SEPARATOR: Separator,
    ComponentType.CONTAINER: Container,
    ComponentType.LABEL: Label,
    ComponentType.FILE_UPLOAD: FileUpload,
    ComponentType.RADIO_GROUP: RadioGroup,
    ComponentType.CHECKBOX_GROUP: CheckboxGroup,
    ComponentType.CHECKBOX: Checkbox
}

class MessageComponentFactory:
    """Represents top-level components."""

    @staticmethod
    def from_dict(data: dict):
        component_type = ComponentType(int(data["type"]))
        model_cls = COMPONENT_MAP.get(component_type)

        if not model_cls:
            raise ValueError(f"Invalid component type: {component_type}")

        return model_cls.from_dict(data)

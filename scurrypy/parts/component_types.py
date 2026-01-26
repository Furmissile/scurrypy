class ActionRowChild: 
    """Marker class for all components that go into an action row.

    !!! tip "Children"
        [`ButtonPart`][scurrypy.parts.components.ButtonPart], 
        [`StringSelectPart`][scurrypy.parts.components.StringSelectPart], 
        [`UserSelectPart`][scurrypy.parts.components.UserSelectPart], 
        [`RoleSelectPart`][scurrypy.parts.components.RoleSelectPart], 
        [`MentionableSelectPart`][scurrypy.parts.components.MentionableSelectPart], 
        [`ChannelSelectPart`][scurrypy.parts.components.ChannelSelectPart]
    """
    ...

class SectionChild: 
    """Marker class for all components that go into a section.

    !!! tip "Children"
        [`TextDisplayPart`][scurrypy.parts.components_v2.TextDisplayPart]
    """
    ...

class SectionAccessoryChild: 
    """Marker class for all components that go into a section accessory.
    
    !!! tip "Children"
        [`ButtonPart`][scurrypy.parts.components.ButtonPart], 
        [`ThumbnailPart`][scurrypy.parts.components_v2.ThumbnailPart]
    """
    ...

class ContainerChild: 
    """Marker class for all components that go into a container.
    
    !!! tip "Children"
        [`ActionRowPart`][scurrypy.parts.components.ActionRowPart], 
        [`TextDisplayPart`][scurrypy.parts.components_v2.TextDisplayPart], 
        [`SectionPart`][scurrypy.parts.components_v2.SectionPart], 
        [`MediaGalleryPart`][scurrypy.parts.components_v2.MediaGalleryPart], 
        [`SeparatorPart`][scurrypy.parts.components_v2.SeparatorPart], 
        [`FilePart`][scurrypy.parts.components_v2.FilePart]
        [`FileUploadPart`][scurrypy.parts.components_v2.FileUploadPart]
    """
    ...

class LabelChild: 
    """Marker class for all components that go into a label.
    
    !!! tip "Children"
        [`TextInputPart`][scurrypy.parts.components.TextInputPart], 
        [`StringSelectPart`][scurrypy.parts.components.StringSelectPart], 
        [`UserSelectPart`][scurrypy.parts.components.UserSelectPart], 
        [`RoleSelectPart`][scurrypy.parts.components.RoleSelectPart], 
        [`MentionableSelectPart`][scurrypy.parts.components.MentionableSelectPart], 
        [`ChannelSelectPart`][scurrypy.parts.components.ChannelSelectPart], 
        [`FileUploadPart`][scurrypy.parts.components_v2.FileUploadPart]
    """
    ...

class ComponentTypes:
    ACTION_ROW = 1
    BUTTON = 2
    STRING_SELECT = 3
    TEXT_INPUT = 4
    USER_SELECT = 5
    ROLE_SELECT = 6
    MENTIONABLE_SELECT = 7
    CHANNEL_SELECT = 8
    SECTION = 9
    TEXT_DISPLAY = 10
    THUMBNAIL = 11
    MEDIA_GALLERY = 12
    FILE = 13
    SEPARATOR = 14
    CONTAINER = 17
    LABEL = 18
    FILE_UPLOAD = 19

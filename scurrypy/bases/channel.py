from ..core.model import DataModel

class GuildChannelCreate(DataModel):
    """Marker base for all guild channel creation payloads.
    
    !!! tip "Variants"
        [`GuildTextChannelPart`][scurrypy.api.channels.GuildTextChannelPart]
        [`GuildAnnouncementChannelPart`][scurrypy.api.channels.GuildAnnouncementChannelPart]
        [`GuildForumChannelPart`][scurrypy.api.channels.GuildForumChannelPart]
    """
    pass

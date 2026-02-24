from scurrypy import Client
from scurrypy.core import MissingField
from scurrypy.api.user import UserModel, GuildMemberModel
from scurrypy.resources import Interaction, Message, Channel, Guild
from scurrypy.events import InteractionEvent

class InteractionContext(Interaction):
    """Useful interaction event info."""

    def __init__(self, bot: Client, event: InteractionEvent):
        super().__init__(bot.http, event.id, event.token)
        self.bot = bot
        self.event = event
        self.data = event.data

    @property
    def user(self) -> UserModel:
        """The invoking user."""
        return self.event.member.user

    @property
    def member(self) -> GuildMemberModel:
        """The invoking user's member."""
        return self.event.member
    
    @property
    def channel(self) -> Channel:
        """Channel resource of the interaction."""
        return self.bot.channel(self.event.channel_id)
    
    @property
    def guild(self) -> Guild:
        """Guild resource of the interaction."""
        if not self.event.guild_id:
            raise MissingField("This event has no associated guild ID.")
        
        return self.bot.guild(self.event.guild_id)

    @property
    def message(self) -> Message:
        """Message resource of the interaction."""
        if not self.event.message:
            raise MissingField("This event has no associated message.")
        
        return self.bot.message(self.event.channel_id, self.event.message.id)

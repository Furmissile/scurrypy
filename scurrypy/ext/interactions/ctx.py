from scurrypy import Client
from scurrypy.resources import Interaction
from scurrypy.events import InteractionEvent

class InteractionContext(Interaction):
    """Useful interaction event info."""

    def __init__(self, bot: Client, event: InteractionEvent):
        super().__init__(bot.http, event.id, event.token)
        self.bot = bot
        self.event = event
        self.data = event.data

    @property
    def user(self):
        """The invoking user."""
        return self.event.member.user

    @property
    def member(self):
        """The invoking user's member."""
        return self.event.member
    
    @property
    def channel(self):
        """Channel resource of the interaction."""
        return self.bot.channel(self.event.channel_id)
    
    @property
    def guild(self):
        """Guild resource of the interaction."""
        return self.bot.guild(self.event.guild_id)

    @property
    def message(self):
        """Message resource of the interaction."""
        return self.bot.message(self.event.channel_id, self.event.message.id)

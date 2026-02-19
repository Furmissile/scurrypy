from scurrypy import Client
from scurrypy.resources import Channel
from scurrypy.events import MessageCreateEvent

class PrefixCommandContext(Channel):
    """Useful message prefix event info."""

    def __init__(self, bot: Client, event: MessageCreateEvent, args: list[str]):
        super().__init__(bot.http, event.channel_id)
        self.bot = bot
        self.event = event
        self.args = args

    @property
    def author(self):
        """Author of the prefix command."""
        return self.event.author

    @property
    def guild(self):
        """Guild resource of the prefix command."""
        return self.bot.guild(self.event.guild_id)

    @property
    def channel(self):
        """Channel resource of the prefix command."""
        return self.bot.channel(self.event.channel_id)

    @property
    def message(self):
        """Message resource of the prefix command."""
        return self.bot.message(self.event.channel_id, self.event.id)

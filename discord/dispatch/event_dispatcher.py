from ..http import HTTPClient
from ..logger import Logger

from ..events.ready_event import *
from ..events.reaction_events import *
from ..events.guild_events import *
from ..events.message_events import *
from ..events.channel_events import *
from ..events.interaction_events import *

from ..resources.message import Message

class EventDispatcher:
    """Central hub for handling Discord Gateway events."""
    RESOURCE_MAP = { # maps discord events to their respective dataclass
        'READY': ReadyEvent,
        
        "MESSAGE_CREATE": MessageCreateEvent,
        "MESSAGE_UPDATE": MessageUpdateEvent,
        'MESSAGE_DELETE': MessageDeleteEvent,

        'MESSAGE_REACTION_ADD': ReactionAddEvent,
        'MESSAGE_REACTION_REMOVE': ReactionRemoveEvent,
        'MESSAGE_REACTION_REMOVE_ALL': ReactionRemoveAllEvent,
        'MESSAGE_REACTION_REMOVE_EMOJI': ReactionRemoveEmojiEvent,

        'CHANNEL_CREATE': GuildChannelCreateEvent,
        'CHANNEL_UPDATE': GuildChannelUpdateEvent,
        'CHANNEL_DELETE': GuildChannelDeleteEvent,

        'CHANNEL_PINS_UPDATE': ChannelPinsUpdateEvent,

        'GUILD_CREATE': GuildCreateEvent,
        'GUILD_UPDATE': GuildUpdateEvent,
        'GUILD_DELETE': GuildDeleteEvent,

        'INTERACTION_CREATE': InteractionEvent

        # and other events...
    }
    """Mapping of event names to respective dataclass."""
    
    def __init__(self, application_id: int, http: HTTPClient, logger: Logger):
        self.application_id = application_id
        """Bot's ID."""

        self._http = http
        """HTTP session for requests."""

        self._logger = logger
        """HTTP session for requests"""

        self._handlers = {}
        """Mapping of event names to handler."""

    def register(self, event_name: str, handler):
        """Registers the given handler to the given event name.
            (Event name must be a valid Discord event)

        Args:
            event_name (str): name of the event
            handler (callable): callback to handle event
        """
        self._handlers[event_name] = handler

    async def dispatch(self, event_name: str, data: dict):
        """Hydrate the corresponding dataclass and call the handler.

        Args:
            event_name (str): name of the event
            data (dict): Discord's raw event payload
        """
        cls = self.RESOURCE_MAP.get(event_name)
        
        if not cls:
            return
        
        if isinstance(cls, Message) and cls.author.id == self.application_id:
            return # ignore bot's own messages
        
        handler = self._handlers.get(event_name, None)
        if handler:
            obj = cls.from_dict(data, self._http)
            await handler(obj)
            self._logger.log_info(f"Event {event_name} Acknowledged.")

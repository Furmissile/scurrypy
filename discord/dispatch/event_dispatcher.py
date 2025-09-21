from importlib import import_module
from ..client_like import ClientLike

from ..resources.message import Message

class EventDispatcher:
    """Central hub for handling Discord Gateway events."""

    RESOURCE_MAP = { # maps discord events to their respective dataclass (lazy loading)
        'READY': ('discord.events.ready_event', 'ReadyEvent'),

        'MESSAGE_CREATE': ('discord.events.message_events', 'MessageCreateEvent')
        
        # and other events...
    }
    
    """Mapping of event names to respective dataclass."""
    
    def __init__(self, client: ClientLike):
        self.application_id = client.application_id
        """Bot's ID."""

        self.bot = client
        """Top-level discord client."""

        self._http = client._http
        """HTTP session for requests."""

        self._logger = client._logger
        """HTTP session for requests"""

        self.config = client.config
        """User-defined bot config for persistent data."""

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
        module_info = self.RESOURCE_MAP.get(event_name)
        
        if not module_info:
            return
        
        module_name, class_name = module_info

        module = import_module(module_name)
        if not module:
            print(f"Cannot find module '{module_name}'!")
            return

        cls = getattr(module, class_name)
        if not cls:
            print(f"Cannot find class '{class_name}'!")
            return
        
        if isinstance(cls, Message) and cls.author.id == self.application_id:
            return # ignore bot's own messages
        
        handler = self._handlers.get(event_name, None)
        if handler:
            obj = cls.from_dict(data, self._http)
            obj.config = self.config
            await handler(self.bot, obj)
            self._logger.log_info(f"Event {event_name} Acknowledged.")

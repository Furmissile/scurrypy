import logging

logger = logging.getLogger('scurrypy')

from scurrypy import Client
from scurrypy.bases import Addon
from scurrypy.enums import EventType
from scurrypy.core import DiscordError
from scurrypy.api.interactions import MessageComponentDataModel, ModalDataModel
from scurrypy.events import InteractionEvent

from .ctx import MessageComponentContext, ComponentModalContext

def _check_func_params(func: callable):
    import inspect
    
    params_len = len(inspect.signature(func).parameters)

    if params_len != 1:
        raise TypeError(
            f"Component handler '{func.__name__}' must accept exactly one parameter (ctx)."
        )

class ComponentsAddon(Addon):
    """Addon that implements automatic registering and decorating component interactions."""

    def __init__(self, client: Client):
        """
        Args:
            client (Client): the bot client object
        """
        self.bot = client

        self.component_handlers = {}
        """Mapping of component custom IDs to handler."""

        client.add_startup_hook(self.on_startup) # wait until start to register commands

    def on_startup(self):
        """Sets up the addon with the client."""

        self.bot.add_event_listener(EventType.INTERACTION_CREATE, self.dispatch)

    def component(self, custom_id: str, *, handler: callable = None):
        if handler is not None:
            _check_func_params(handler)
            self.component_handlers[custom_id] = handler
        else:
            def decorator(func):
                _check_func_params(func)
                self.component_handlers[custom_id] = func
            return decorator
    
    # helpers purly for ergonomics
    def button(self, custom_id: str, *, handler: callable = None):
        """Register and route button interactions.

        Args:
            custom_id (str): custom ID of button
                !!! warning "Important"
                    Must match the `custom_id` set where the component was created.
            handler (callable, optional): callback for the command (if not a decorator)
        """
        return self.component(custom_id, handler=handler)

    def select(self, custom_id: str, *, handler: callable = None):
        """Register and route select menu interactions.

        Args:
            custom_id (str): custom ID of select menu
                !!! warning "Important"
                    Must match the `custom_id` set where the component was created.
            handler (callable, optional): callback for the command (if not a decorator)
        """
        return self.component(custom_id, handler=handler)

    def modal(self, custom_id: str, *, handler: callable = None):
        """Register and route modal interactions.

        Args:
            custom_id (str): custom ID of modal
                !!! warning "Important"
                    Must match the `custom_id` set where the component was created.
            handler (callable, optional): callback for the command (if not a decorator)
        """
        return self.component(custom_id, handler=handler)

    def _get_handler(self, name: str):
        """Helper function for fetching a handler by `fnmatch`."""

        import fnmatch
        for k, v in self.component_handlers.items():
            if fnmatch.fnmatch(name, k):
                return v
        return False

    async def dispatch(self, event: InteractionEvent):
        """Dispatch a response to an `INTERACTION_CREATE` event

        Args:
            event (InteractionEvent): interaction event object
        """
        # only respond to component interactions
        data = event.data

        if not isinstance(data, (MessageComponentDataModel, ModalDataModel)):
            return # ignore non-component interactions

        name = data.custom_id
        handler = self._get_handler(name)

        if not handler:
            logger.warning(f"No handler registered for interaction '{name}'")
            return
                
        if isinstance(data, MessageComponentDataModel):
            ctx = MessageComponentContext(self.bot, event)
        
        elif isinstance(data, ModalDataModel):
            ctx = ComponentModalContext(self.bot, event)

        try:
            await handler(ctx)
            logger.info(f"Interaction '{name}' Acknowledged.")
        except DiscordError as e:
            logger.error(f"Error in interaction '{name}': {e}")
        except Exception as e:
            logger.exception(f"Unhandled error in interaction '{name}': {e}")

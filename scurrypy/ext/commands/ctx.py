from scurrypy.api.interactions import (
    ApplicationCommandDataModel, 
    AutocompleteApplicationCommandDataModel,
)

from ..interactions.ctx import InteractionContext

class ApplicationCommandContext(InteractionContext):
    data: ApplicationCommandDataModel

class AutocompleteApplicationCommandContext(InteractionContext):
    data: AutocompleteApplicationCommandDataModel

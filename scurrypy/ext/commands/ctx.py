from scurrypy.api.interactions import (
    ApplicationCommandDataModel, 
    AutocompleteApplicationCommandDataModel,
)

from ..interactions.ctx import InteractionContext

class CommandContext(InteractionContext):
    ...

class ApplicationCommandContext(CommandContext):
    data: ApplicationCommandDataModel

class AutocompleteApplicationCommandContext(CommandContext):
    data: AutocompleteApplicationCommandDataModel

from scurrypy.api.interactions import MessageComponentDataModel, ModalDataModel

from ..interactions.ctx import InteractionContext

class ComponentContext(InteractionContext):
    pass

class MessageComponentContext(ComponentContext):
    data: MessageComponentDataModel

class ComponentModalContext(ComponentContext):
    data: ModalDataModel

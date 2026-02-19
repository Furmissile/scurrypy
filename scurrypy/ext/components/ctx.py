from scurrypy.api.interactions import MessageComponentDataModel, ModalDataModel

from ..interactions.ctx import InteractionContext

class MessageComponentContext(InteractionContext):
    data: MessageComponentDataModel

class ComponentModalContext(InteractionContext):
    data: ModalDataModel

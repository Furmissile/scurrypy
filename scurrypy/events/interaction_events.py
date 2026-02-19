from dataclasses import dataclass, field

from .base_event import Event

from ..bases.interaction import InteractionData

from ..enums.interaction import InteractionType

from ..api.interactions.interaction import InteractionModel, ApplicationCommandDataModel, MessageComponentDataModel, ModalDataModel

@dataclass
class InteractionEvent(Event, InteractionModel):

    data: InteractionData = field(init=False, default=None)
    """Interaction response data. Can be one of `InteractionData`[scurrypy.bases.InteractionData]'s variants."""

    @classmethod
    def from_dict(cls, data: dict):

        obj = super().from_dict(data) # InteractionModel's DataModel

        interaction_data = data.get("data")
        interaction_type = data.get("type")

        match interaction_type:
            case InteractionType.APPLICATION_COMMAND | InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE:
                obj.data = ApplicationCommandDataModel.from_dict(interaction_data)
            case InteractionType.MESSAGE_COMPONENT:
                obj.data = MessageComponentDataModel.from_dict(interaction_data)
            case InteractionType.MODAL_SUBMIT:
                obj.data = ModalDataModel.from_dict(interaction_data)
        
        return obj

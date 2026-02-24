from dataclasses import dataclass, field

from .base_event import Event

from ..bases.interaction import InteractionData

from ..enums.interaction import InteractionType
from ..enums.events import EventType

from ..api.interactions.interaction import InteractionModel, ApplicationCommandDataModel, MessageComponentDataModel, ModalDataModel

from ..core.types import HTTPResponse
from typing import Self

@dataclass
class InteractionEvent(Event, InteractionModel):

    dispatch_name = EventType.INTERACTION_CREATE

    data: InteractionData = field(init=False)
    """Interaction response data. Can be one of `InteractionData`[scurrypy.bases.InteractionData]'s variants."""

    @classmethod
    def from_dict(cls, data: HTTPResponse) -> Self:
        assert isinstance(data, dict)

        obj = super().from_dict(data) # InteractionModel's DataModel

        interaction_data = data["data"]
        interaction_type = data["type"]

        match interaction_type:
            case InteractionType.APPLICATION_COMMAND | InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE:
                obj.data = ApplicationCommandDataModel.from_dict(interaction_data)
            case InteractionType.MESSAGE_COMPONENT:
                obj.data = MessageComponentDataModel.from_dict(interaction_data)
            case InteractionType.MODAL_SUBMIT:
                obj.data = ModalDataModel.from_dict(interaction_data)
        
        return obj

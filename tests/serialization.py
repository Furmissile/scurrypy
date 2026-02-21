# --- DESERIALIZE/SERIALIZE ---
from scurrypy.api.messages import Embed

embed_data = {
    'title': 'my embed',
    'color': '1234567',
    'fields': [
        {
            'name': 'demo field',
            'value': 'demo value',
            'inline': 'false'
        },
        {
            'name': 'demo field',
            'value': 'demo value',
            'inline': 'true'
        }
    ]
}

embed = Embed.from_dict(embed_data)
assert embed.title == 'my embed'
assert embed.color == 1234567
assert embed.fields[0].name == 'demo field'
assert embed.fields[0].value == 'demo value'
assert embed.fields[0].inline == False
assert embed.fields[1].inline == True

embed_dict = embed.to_dict()
assert embed_dict['fields'][0]['inline'] == False
assert embed_dict['fields'][1]['inline'] == True

# --- FLAGS ---
from scurrypy.api.messages import MessagePart, MessageFlags

msg_data = {
    'content': 'my message',
    'flags': '68'
}

msg = MessagePart.from_dict(msg_data)

assert msg.content == 'my message'
assert MessageFlags.EPHEMERAL in msg.flags

# --- TYPING ---

from scurrypy.core import DataModel
from dataclasses import dataclass

@dataclass
class A(DataModel):
    int_field: int
    str_field: str
    bool_field: bool
    missing_field: int | None
    maybe_field: int | None
    # invalid_union: int | None | str # -- should throw exception

a = A.from_dict({
    'int_field': '123',
    'str_field': 'string',
    'bool_field': 'false',
    # missing field
    'maybe_field': '456',
    'invalid_union': '789'
})

assert a.int_field == 123
assert a.str_field == 'string'
assert a.bool_field == False
assert a.missing_field is None
assert a.maybe_field == 456

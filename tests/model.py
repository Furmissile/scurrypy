"""
  Test converting dict to dataclass using DataModel
"""
from dataclasses import dataclass
from scurrypy.core.model import DataModel

@dataclass
class TestComponent(DataModel):
    type: int
    content: str

@dataclass
class Test(DataModel):
    flags: int
    components: list[TestComponent]

t = Test.from_dict({
	"flags": 32768,
	"components": [
		{
			"type": 10,
			"content": "This is a Text Display component."
		},
		{
			"type": 10,
			"content": "This is another Text Display component!"
		}
	]
})

assert t.flags is not None
assert t.components
assert all(c.content is not None for c in t.components)


"""
  Test converting dataclass to dict using DataModel
"""
import scurrypy

a = scurrypy.ActionRowPart(
    [
        scurrypy.Button(
			style=scurrypy.ButtonStyles.PRIMARY,
			custom_id='example',
			emoji=scurrypy.EmojiModel('❤️')
		),
        scurrypy.Button(
			style=scurrypy.ButtonStyles.SECONDARY,
			custom_id='another',
		)
    ]
).to_dict()

assert a['components']

assert a['components'][0]['emoji']['name'] == '❤️'

assert a['components'][1]['style'] == scurrypy.ButtonStyles.SECONDARY

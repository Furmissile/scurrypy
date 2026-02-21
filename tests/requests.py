from scurrypy.core.http import HTTPClientProtocol

class MockHTTPClient(HTTPClientProtocol):
    def __init__(self, responses: dict):
        self.responses = responses  # endpoint -> response
        self.requests = []  # track what was called

    async def start(self, token: str): ...
    async def close(self): ...
    
    async def request(self, method, endpoint, *, data=None, params=None, files=None, assets=None):
        self.requests.append((method, endpoint, data))
        assert self.responses.get(endpoint) is not None # make sure the response exists
        return self.responses.get(endpoint)

from scurrypy.api.messages import MessageModel

async def test_post(mock: MockHTTPClient):
    from scurrypy.resources import Channel
    from scurrypy.api.messages import MessagePart

    channel = Channel(mock, 123)
    msg_create = MessagePart(content='hello')
    msg = await channel.send(msg_create)

    assert isinstance(msg, MessageModel)
    assert msg.content == 'hello'
    assert ('POST', '/channels/123/messages', msg_create.to_dict()) in mock.requests

async def test_get(mock: MockHTTPClient):
    from scurrypy.resources import Message

    message = Message(mock, 999, 123)
    msg = await message.fetch()

    assert isinstance(msg, MessageModel)
    assert msg.content == 'hello'
    assert ('GET', '/channels/123/messages/999', None) in mock.requests # GET requires NO data

mock = MockHTTPClient({
    '/channels/123/messages': {
        'id': '999', 
        'content': 'hello', 
        'channel_id': '123'
    },
    '/channels/123/messages/999': {
        'id': '999', 
        'content': 'hello',
        'channel_id': '123'
    }
})

import asyncio
asyncio.run(test_post(mock))
asyncio.run(test_get(mock))

## __<center> ScurryPy </center>__

[![PyPI version](https://badge.fury.io/py/scurrypy.svg)](https://badge.fury.io/py/scurrypy)

A lightweight, fully readable Discord API framework built to accommodate everything from basic bots to custom frameworks.

While ScurryPy powers many squirrel-related shenanigans, it works just as well for game bots, interactive components, and educational projects.

## Features
* Easy to extend and build frameworks on top
* Lightweight core (<1000 lines)
* Command, and event handling
* Unix shell-style wildcards for component routing
* Declarative style using decorators
* Supports both legacy and new features
* Respects Discord's rate limits
* No `__future__` hacks to avoid circular import
* Capable of sharding

## Getting Started

*Note: This section also appears in the documentation, but here are complete examples ready to use with your bot credentials.*

### Installation

To install the ScurryPy package, run:

```bash
pip install scurrypy
```

## Minimal Slash Command

The following demonstrates building and responding to a slash command.

```py
import scurrypy

client = scurrypy.Client(
    token='your-token',
    application_id=APPLICATION_ID  # your bot's application ID
)

@client.command(
    scurrypy.SlashCommand('example', 'Demonstrate the minimal slash command!'), 
    GUILD_ID  # must be a guild ID your bot is in
)
async def example(bot: scurrypy.Client, event: scurrypy.InteractionEvent):
    await event.interaction.respond(f'Hello, {event.interaction.member.user.username}!')

client.run()
```

## Minimal Prefix Command (Legacy)

The following demonstrates building and responding to a message prefix command.

```py
import scurrypy

client = scurrypy.Client(
    token='your-token',
    application_id=APPLICATION_ID,  # your bot's application ID
    intents=scurrypy.set_intents(message_content=True),
    prefix='!'  # your custom prefix
)

@client.prefix_command("ping")
async def on_ping(bot: scurrypy.Client, event: scurrypy.MessageCreateEvent):
    await event.message.send("Pong!")

client.run()
```

## Building on Top of ScurryPy

ScurryPy is designed to be easy to extend with your own abstractions.

The following demonstrates integrating a custom cache into your client configuration:

```py
class CacheProtocol(Protocol):
    async def get_user(self, user_id: int) ...

    # and the rest...

class MyCache(CacheProtocol):
    # your implementation...

class MyConfig(BaseConfig):
    cache: MyCache
    # other stuff here...

client = scurrypy.Client(
    token = 'your-token',
    application_id = 123456789012345,
    config = MyConfig()
)
```

## Like What You See?
Explore the full [documentation](https://furmissile.github.io/scurrypy) for more examples, guides, and API reference.

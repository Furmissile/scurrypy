# __ScurryPy__

[![PyPI version](https://badge.fury.io/py/scurrypy.svg)](https://badge.fury.io/py/scurrypy)

A dataclass-driven Discord API wrapper in Python!

While this wrapper is mainly used for various squirrel-related shenanigans, it can also be used for more generic bot purposes.

## Features
* Easy to extend
* Command, and event handling
* Unix shell-style wildcards for component routing
* Declarative style using decorators
* Supports both legacy and new features
* Respects Discord's rate limits
* No `__future__` hacks to avoid circular import
* Capable of sharding

## Benchmarks
Not convinced ScurryPy has a place among top libraries? See the benchmarks below!

### Test Environment

- **Python**: 3.11.6
- **OS**: Windows 11

### Results Summary

```
Library         Time (ms)    Memory Δ (MB)      Objects
--------------------------------------------------------
scurrypy              8.9             0.44         1417
hikari             1710.3            27.67        53658
discord             252.5             7.64        14099
disnake             185.9             6.31        12111
```

*(See `tests/benchmark.py` for how this test was done.)*

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

## Like What You See?
Explore the full [documentation](https://furmissile.github.io/scurrypy) for more examples, guides, and API reference.

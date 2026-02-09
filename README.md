<div align='center'>

## ScurryPy

[![PyPI version](https://badge.fury.io/py/scurrypy.svg)](https://badge.fury.io/py/scurrypy)
[![Discord](https://img.shields.io/discord/905167903224123473?style=plastic&logo=discord&logoColor=ffffff&color=5865F2)](https://discord.gg/D4SdHxcujM)

<img
src="assets/banner.png"
width="450"
alt="Fire-breathing squirrel"
/>

✨ **Clarity over magic**: build a bot that lasts ✨

</div>

## Features

* Lightweight core
* Rate limit handling
* Automatic session & gateway management
* Automatic sharding
* Predictable event models and resource classes

Your focus is building what you want instead of fighting a framework.

## Installation

Install ScurryPy with pip:

```bash
pip install scurrypy
```

## Examples

The following examples are quick drop-in starters if you wish to try ScurryPy.

> [!TIP]
> It is recommended to use a `.env` file for bot tokens. More details about using a `.env` file [here](https://scurry-works.github.io/scurrypy/getting_started/start_here/).

### Slash Command

```python
# Set TOKEN, APP_ID (bot user ID), and GUILD_ID (for guild command)

# --- Core library imports ---
from scurrypy import Client, EventTypes, InteractionEvent, SlashCommandPart

client = Client(TOKEN)

# --- Setup bot ---
async def create_commands():
    """Create a command for the bot APP_ID in guild GUILD_ID."""
    await client.guild_command(APP_ID, GUILD_ID).create(
        SlashCommandPart("greet", "Greet the bot!")
    )

client.add_startup_hook(create_commands)

async def on_greet(event: InteractionEvent):
    """Respond to the created slash command."""
    if event.data.name != "greet":
        return

    await client.interaction(event.id, event.token).respond("Hello!")

client.add_event_listener(EventTypes.INTERACTION_CREATE, on_greet)

# --- Run the bot ---
client.run()
```

### Prefix Command (Legacy)

```python
# Set TOKEN

# --- Core library imports ---
from scurrypy import Client, Intents, EventTypes, MessageCreateEvent

client = Client(TOKEN, Intents.set(message_content=True)) # requires MESSAGE_CONTENT intent

# --- Setup bot ---
async def on_ping(event: MessageCreateEvent):
    """Respond to the '!ping' command."""
    if not event.content:
        return # ignore empty messages

    if not event.content.startswith('!ping'):
        return # ignore messages that are not the command

    await client.channel(event.channel_id).send("Pong!")

client.add_event_listener(EventTypes.MESSAGE_CREATE, on_ping)

# --- Run the bot ---
client.run()
```

## Dependencies

ScurryPy has exactly 3 required dependencies:
- aiohttp (HTTP client)
- websockets (Gateway connection)  
- aiofiles (Async file operations)

These dependencies are automatically installed with ScurryPy's pip package.

## Learn More

Explore the full [documentation](https://scurry-works.github.io/scurrypy) for more examples, guides, and API reference.

See the [manifesto](https://scurry-works.github.io/scurrypy/manifesto) section for details!

**Switching from discord.py?** 
Check out the [Migration Guide](https://scurry-works.github.io/scurrypy/getting_started/migrating) to see the difference.

**Got some questions?**
Check out the [FAQ](https://scurry-works.github.io/scurrypy/faq) page for commonly asked questions!

**Looking for changes?** 
See the [Changelog](https://github.com/scurry-works/scurrypy/blob/main/CHANGELOG.md).

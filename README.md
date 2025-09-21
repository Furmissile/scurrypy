# __Welcome to ScurryPy__

[![PyPI version](https://badge.fury.io/py/scurrypy.svg)](https://badge.fury.io/py/scurrypy)

Yet another Discord API wrapper in Python!  

While this wrapper is mainly used for various squirrel-related shenanigans, it can also be used for more generic bot purposes.

## Features
* Command and event handling
* Declarative style using decorators
* Supports both legacy and new features
* Respects Discord's rate limits

## Some things to consider...
* This is an early version — feedback, ideas, and contributions are very welcome! That said, there may be bumps along the way, so expect occasional bugs and quirks.
* Certain features are not yet supported, while others are intentionally omitted. See the [docs](https://furmissile.github.io/scurrypy) for full details.

## Getting Started
*Note: This section also appears in the documentation, but here are complete examples ready to use with your bot credentials.*

### Installation
To install the ScurryPy package, run:
```bash
pip install scurrypy
```

### Minimal Slash Command
The following demonstrates building and responding to a slash command.

*Note: Adjust `dotenv_path` if your `.env` file is not in the same directory as this script.*

```python
import discord, os
from dotenv import load_dotenv

load_dotenv(dotenv_path='./path/to/env')

client = discord.Client(
    token=os.getenv("DISCORD_TOKEN"),
    application_id=APPLICATION_ID  # replace with your bot's user ID
)

@client.command(
    command=discord.SlashCommand(
        name='example',
        description='Demonstrate the minimal slash command!'
    ),
    guild_id=GUILD_ID  # must be a guild ID your bot is in
)
async def example(bot: discord.Client, event: discord.InteractionEvent):
    await event.interaction.respond(f'Hello, {event.interaction.member.user.username}!')

client.run()
```

### Minimal Prefix Command (Legacy)
The following demonstrates building and responding to a message prefix command.

```python
import discord, os
from dotenv import load_dotenv

load_dotenv(dotenv_path='./path/to/env')

client = discord.Client(
    token=os.getenv("DISCORD_TOKEN"),
    application_id=APPLICATION_ID,  # replace with your bot's user ID
    intents=discord.set_intents(message_content=True),
    prefix='!'  # your custom prefix
)

@client.prefix_command
async def ping(bot: discord.Client, event: discord.MessageCreateEvent):
    # The function name is the name of the command
    await event.message.send("Pong!")

client.run()
```

## Like what you see?
Check out the full [documentation](https://furmissile.github.io/scurrypy) for more examples, guides, and API reference!

# __Welcome to ScurryPy__

[![PyPI version](https://badge.fury.io/py/scurrypy.svg)](https://badge.fury.io/py/scurrypy)

Yet another Discord API wrapper in Python!

While this wrapper is mainly used for various squirrel-related shenanigans, it can also be used for more generic bot purposes.

## Features
* Command and event handling
* Declarative style using decorators
* Supports both legacy and new features
* Respects Discord's rate limits

## Something things to consider...
* This is an early version — feedback, ideas, and contributions are welcome! With that said, there will be bumps in the road so expect bugs and other flaws!
* Some features are not yet supported, such as sharding and automod, while others, like voice, will never be supported. While this library can handle many of your basic needs, common features such as sharding or auto-mod actions are not yet implemented. See the [license](LICENSE) for details on usage.


## Getting Started
While this tab shows up in the docs, here are some complete examples where all you need to do is pop in your bot's credentials!

## Installation
To install the ScurryPy package, run:
```bash
pip install scurrypy
```

## Minimal Slash Command
The following demonstrates building and responding to a slash command.
```python
import discord, os
from dotenv import load_dotenv

load_dotenv(dotenv_path='./path/to/env') # omit argument if your env file is on the same level

bot = discord.Client(
    token=os.getenv("DISCORD_TOKEN"),
    application_id=1234567890 # replace with your bot's user ID
)

@bot.command(
    command=discord.SlashCommand(name='example', description='Demonstrate the minimal slash command!'),
    guild_id=GUILD_ID # must be a guild ID your bot is in!
)
async def example(event: discord.InteractionEvent):
    await event.interaction.respond(f'Hello, {event.interaction.member.user.username}!')

bot.run()
```

## Minimal Prefix Command (Legacy)
The following demonstrates building and responding to a message prefix command.
```python
import discord, os
from dotenv import load_dotenv

load_dotenv(dotenv_path='./path/to/env') # omit argument if your env file is on the same level

bot = discord.Client(
    token=os.getenv("DISCORD_TOKEN"),
    application_id=1234567890, # replace with your bot's user ID
    intents=discord.set_intents(message_content=True),
    prefix='!' # your custom prefix
)

@bot.prefix_command
async def ping(event: discord.MessageCreateEvent): # the function name is the name of the command!
    await event.message.send(f"Pong!")

bot.run()
```

## Like what you see?
See the [docs](https://furmissile.github.io/scurrypy) for more!

# __ScurryPy__

[![PyPI version](https://badge.fury.io/py/scurrypy.svg)](https://badge.fury.io/py/scurrypy)

> **Official Repository**  
> This is the original and official repository of **ScurryPy**, maintained by [Furmissile](https://github.com/Furmissile).  
> Forks and community extensions are welcome under the project’s license and attribution guidelines.

A dataclass-driven Discord API wrapper in Python!

While this wrapper is mainly used for various squirrel-related shenanigans, it can also be used for more generic bot purposes.

## Features
* Command, and event handling
* Unix shell-style wildcards for component routing
* Declarative style using decorators
* Supports both legacy and new features
* Respects Discord’s rate limits

## Notes & Early Status
* This is an early version — feedback, ideas, and contributions are very welcome! That said, there may be bumps along the way, so expect occasional bugs and quirks.  
* Certain features are not yet supported, while others are intentionally omitted. See the [docs](https://furmissile.github.io/scurrypy) for full details.  

## Getting Started
*Note: This section also appears in the documentation, but here are complete examples ready to use with your bot credentials.*

### Installation
To install the ScurryPy package, run:
```bash
pip install scurrypy
```

## Minimal Slash Command
The following demonstrates building and responding to a slash command.

*Note: Adjust `dotenv_path` if your `.env` file is not in the same directory as this script.*

```py
import scurrypy, os
from dotenv import load_dotenv

load_dotenv(dotenv_path='./path/to/env')

client = scurrypy.Client(
    token=os.getenv("DISCORD_TOKEN"),
    application_id=APPLICATION_ID  # your bot’s application ID
)

@client.command(
    command=scurrypy.SlashCommand(
        name='example',
        description='Demonstrate the minimal slash command!'
    ),
    guild_ids=GUILD_ID  # must be a guild ID your bot is in
)
async def example(bot: scurrypy.Client, event: scurrypy.InteractionEvent):
    await event.interaction.respond(f'Hello, {event.interaction.member.user.username}!')

client.run()
```

## Minimal Prefix Command (Legacy)
The following demonstrates building and responding to a message prefix command.
```py
import scurrypy, os
from dotenv import load_dotenv

load_dotenv(dotenv_path='./path/to/env')

client = scurrypy.Client(
    token=os.getenv("DISCORD_TOKEN"),
    application_id=APPLICATION_ID  # your bot’s application ID
    intents=scurrypy.set_intents(message_content=True),
    prefix='!'  # your custom prefix
)

@client.prefix_command
async def ping(bot: scurrypy.Client, event: scurrypy.MessageCreateEvent):
    # The function name is the name of the command
    await event.message.send("Pong!")

client.run()
```

## Contribution and Fork Policy
ScurryPy follows a simple philosophy: **clarity, simplicity, and direct interaction with the Discord API**.
It favors explicit, dataclass-driven design over heavy abstraction — and contributions should stay true to that style.

This is a community-supported project guided by the design and principles of **Furmissile**.
You are welcome to explore, modify, and extend the codebase under the terms of its license — but please follow these guidelines to ensure proper attribution and clarity.

### You May
* Fork this repository for personal or collaborative development.
* Submit pull requests for bug fixes or new features that align with ScurryPy’s goals.
* Reuse parts of the code in your own projects, provided attribution is preserved.

### You May NOT
* Remove or alter existing copyright notices or attributions.
* Present a fork as the official ScurryPy project.
* Use the name “ScurryPy” or its documentation to promote a fork without permission.

If you plan to make substantial changes or release your own variant:
* Rename the fork to avoid confusion (e.g., `scurrypy-plus` or `scurrypy-extended`).
* Add a note in your README acknowledging the original project:
> "This project is a fork of [ScurryPy](https://github.com/Furmissile/scurrypy)
 by Furmissile."

 ## License
 This project is licensed under the Furmissile License, which allows viewing, modification, and redistribution with proper attribution.

See the [License](./LICENSE) for details.

## Like What You See?
Explore the full [documentation](https://furmissile.github.io/scurrypy) for more examples, guides, and API reference.

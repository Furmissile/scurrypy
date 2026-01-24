# Changelog

This changelog documents all notable and breaking changes to ScurryPy.

## [0.17.0] - Jan 2026

### Breaking Changes

* Renamed: channel events. Removed `Guild` prefix.
    * The event is for any channel type
* Removed: Channel resource split. Now just the Channel resource.
    * Splitting Channel was not justified.
* Removed: `ReactionType` (unused)
* Removed: `guild` pattern from `Guild` resource functions
* Renamed: `UnavailableGuild` to `UnavailableGuildModel`

### Changed

* Added: Thread events.
* Resources that fire events now say what events are fired.
* Fixed: bot reconnects on normal closure if not cancelled by user
* Revised ordering of reconnection and logic
* Gateway now says:
    * if error due to connection: reconnect + backoff
    * if reconnecting + `RESUME` or `INVALID_SESSION`: reconnect
    * if normal closure by discord: reconnect
    * if normal closure by user: disconnect
* Added: `Message.fetch_emoji_reactions` and `Message.remove_emoji_reaction`. This completes the `Message` resource.
* Added:
    * `Channel.follow`
    * `Channel.bulk_delete_messages`
    * `Channel.fetch_invites`
    * `Channel.create_invite`
    * `Channel.fetch_public_archived_threads`
    * `Channel.fetch_private_archived_threads`
    * `Channel.fetch_joined_private_archived_threads`
    This completes the `Channel` resource.

* New resource: `Invite`

* Added:
    * `Guild.edit`
    * `Guild.fetch_active_threads`
    * `Guild.search_members`
    * `Guild.edit_member`
    * `Guild.remove_member`
    * `Guild.fetch_ban`
    * `Guild.fetch_bans`
    * `Guild.create_ban`
    * `Guild.remove_ban`
    * `Guild.bulk_create_ban`
    * `Guild.fetch_role_member_counts`
    * `Guild.fetch_invites`
    * `Guild.fetch_invites_with_metadata`
    * `Guild.fetch_integrations`
    * `Guild.delete_integration`
    * `Guild.fetch_welcome_screen`
    * `Guild.edit_welcome_screen`
    * `Guild.fetch_onboarding`

* New parts: 
    * `BulkGuildBanPart`
    * `ThreadFromMessagePart`
    * `ThreadWithoutMessagePart`
    * `DefaultReactionPart`
    * `TagPart`
    * `BulkGuildBanPart`
    * `WelcomeScreenChannelPart`
    * `InvitePart`
    

## [0.16.0] - Jan 2026

### Breaking Changes

* Removed: `ImageData.uri` 
    * the uri code is factored into `to_dict`
* New category: `params/` for modifying resources. Used internally by resources.
* Removed: `Message.send` in favor of `Channel.send`
* Renamed: `resources/commands.py` to `resources/command.py`
* `Channel` resource has been split into `ThreadChannel` and `GuildChannel` with `Channel` as a base class.
* `Command` resource has been split into `GuildCommand` and `GlobalCommand` with `Command` as a base class.

* Moving forward, params are for modifying, function parameters are for querying, and parts are for creating.

## [0.15.0]

### Breaking Changes

* Renamed all `modify` resource functions to `edit`
* All endpoints except fetching now require a part.

### Changed

* New endpoints:
    * `GuildEmoji.create`, `GuildEmoji.update`, `GuildEmoji.delete` - this completes the `GuildEmoji` resource
    * `Channel.edit` now accepts DM, thread, and guild channel.
    * Channel threads

* New Parts:
    * `CreateBotEmoji`, `EditBotEmoji`, `CreateGuildEmoji`, `EditGuildEmoji`

* New permissions:
    * `MANAGE_GUILD_EXPRESSIONS`, `CREATE_GUILD_EXPRESSIONS`

* Fixed: reconnection logic
    * `seq` was being set on every HELLO event

* Patched: contributing guide to better explain how endpoints are divided among resources.

* Revised and Corrected: resource docstrings

* Moved: `PinnedMessageModel` from `scurrypy.models.channel` -> `scurrypy.models.message`

## [0.14.0]

### Changed

* New resource: `ImageData`, used for images like emojis, guild icons, banners, etc.

* New endpoints:
    * `BotEmoji.create`, `BotEmoji.modify`, `BotEmoji.delete` - this completes the `BotEmoji` resource

* Fixed various docstring formatting.

* Fixed exponential reconnect for the gateway.
    * Reconnect time now resets once `READY` is fired.

* All fields in `parts/` are now set to None by default.
    * This effectively makes all part fields deferrable for maximum flexibility.

* `EmbedField.inline` now defaults to `False`.

* Removed the unused event class `HelloEvent`.

* Merged ComponentTypes + ComponentV2Types to ComponentTypes

## [0.13.0] - Dec 2025

### Breaking Changes

* `Client.register_guild_commands` and `Client.register_global_commands` have been removed in favor of the `Commands` resource.

### Changed

* New resource: `Commands`.
    * Ex.
        Old:
        ```py
        async def on_register_commands():
            await client.register_guild_commands(APP_ID, commands, guild_ids=GUILD_ID)
        ```

        New:
        ```py
        async def on_register_commands():
            await client.command(APP_ID, GUILD_ID).create_command(command)
        ```

## [0.12.0]

### Changed

* Added: `resolved` field to interaction data for efficient access to resolved objects
    * No API calls needed for USER/ROLE/CHANNEL command options
    * Attachment options now fully supported

* Clarified `ApplicationCommandOptionData.value` type annotation and added conversion guidance

* Bug fix: Boolean conversion in DataModel (string "false" now correctly converts to False)

## [0.11.0]

### Breaking Changes

User was patched to be more bot specific. Some endpoints are not accessible to bots.

* `User.fetch_guilds` endpoint is no longer a method
    * this is a user endpoint and ScurryPy does not support User tokens

### Changes

* Bug fix: `User.fetch_guild_member` endpoint corrected

## [0.10.1]

### Changes

Logging has been improved for finer grained control.

* Gateway heartbeat logs are now emitted at `DEBUG` level.

## [0.10.0]

### Changes

Logging has been improved for finer grained control.

* Events not registered by the user are now `DEBUG` messages.

## [0.9.0]

### Breaking Changes

The handling of `application_id` has been refactored and is now passed explicitly to command registration APIs.

* `Client.__init__`
    * before: `Client(token, application_id, intents, logger)`
    * after: `Client(token, intents)`

* `BaseClient.register_guild_commands`
    * before: `register_guild_commands(commands, guild_ids)`
    * after: `register_guild_commands(application_id, commands, guild_ids)`

* `BaseClient.register_global_commands`
    * before: `register_global_commands(commands)`
    * after: `register_global_commands(application_id, commands)`

* `BaseClient.bot_emoji`
    * before: `bot_emoji()`
    * after: `bot_emoji(application_id)`

### Changed

* Scurrypy's Logger module has been replaced with Python's standard `logging` module.
    * Scurrypy no longer configures logging by default. Users may configure logging as needed.
    * See [Logging](https://scurry-works.github.io/scurrypy/logging) for details.

* New class: `EventTypes`. This class is a convenience class to prevent typos in event registration.
    * Ex.
        ```py
        from scurrypy import Client, EventTypes, MessageCreateEvent

        client = Client(...)

        async def on_message_create(event: MessageCreateEvent): ...

        client.add_event_listener(EventTypes.MESSAGE_CREATE, on_message_create)
        ```

## [0.8.8.2]

### Changed
* Corrected `FileUpload`: `component: LabelChild` is supposed to be `custom_id: str`.
See [FileUpload](https://scurry-works.github.io/scurrypy/api/ui_components/#scurrypy.parts.components_v2.FileUpload) for the updated version.

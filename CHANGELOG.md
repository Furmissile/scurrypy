# Changelog

This changelog documents all notable and breaking changes to ScurryPy.

## [0.20.2] - Feb 2026

### Changed

* Fixed: `ModalData.data` should be and is now `ModalData.resolved`
* Fixed: Components now inherit correct marker types
* Fixed: `HTTPClient.request` now raises `DiscordError` instead of returning `None`
    * Now you can catch `DiscordError` in your own code if needed
* `DiscordError.full_message` is now a class attribute
    * Now you can access the error you see in the console
* Fixed: `DataModel.from_dict` now accepts raw booleans, not just string

## [0.20.1] - Feb 2026

### Changed

* Gateway heartbeats now include latency estimates (not averaged)
* Fixed: `Client.global_command` and `Client.guild_command` args
* Silenced websockets, aiohttp, and asyncio debug messages by default
* Fixed: when passing `MessagePart` to a function like `Channel.send` and then using the `flags` param, flags were not set.
* Fixed: `Channel.send` now accepts flags.

## [0.20.0] - Jan 2026

### Breaking Changes

* Renamed: `RoleColorsPart` to `GuildRoleColorsPart` for easier discoverability

### Changes

* Client.__init__ no longer requires kwargs to instantiate.
    * For example, instead of `Client(token=TOKEN)`, it's just `Client(TOKEN)`
    * This is NOT a breaking change because it does not impact user code.

* Bug fix: Parameters with objects now get converted to a dict if used.

## [0.19.0] - Jan 2026

### Breaking Changes

* Renamed event: `GuildIntegrationUpdateEvent` to `GuildIntegrationsUpdateEvent` (with the 's')

* `User` resource now only takes ID for certain endpoints.
    * ID is no longer required to instantiate the dataclass.

### Changed

* Client now exposes a public http client that is a ref to its private http client
    * Users can now use the http client directly for missing endpoints

* Added new events:
    * `GuildIntegrationCreateEvent`
    * `GuildIntegrationUpdateEvent`
    * `ThreadMemberUpdateEvent`
    * `ThreadListSyncEvent`
    * `UserUpdateEvent`

* Reorganized events for easier navigation
    * NOTE: This does NOT impact user code.

* New `User` endpoints:
    * `User.modify_current_user`
    * `User.leave_guild`
    * `User.create_dm`

## [0.18.0] - Jan 2026

### Breaking Changes

* `Attachment` (now `AttachmentPart`) is now in its own file.
* Renamed: **ALL** parts without the `Part` suffix now have the `Part` suffix!
* `Message.edit` and `Interaction.update` now take `EditMessageParams` instead of `MessagePart`
* ScurryPy no longer validates parameter types. This must be checked by frameworks or bots.
    * **NOTE:** The only exceptions are if Discord's errors are cryptic or there's a legitimate reason to confuse types.
* Renamed intent: `GUILD_EMOJIS_AND_STICKERS` to `GUILD_EXPRESSIONS`

### Changed

* Added endpoint `Guild.edit_onboarding`
* New parts: `OnboardingPromptOptionPart` and `OnboardingPromptPart`
* Fixed: docstring formats
* Fixed: `Message.fetch_emoji_reactions` to actually include parameters
* Added permissions: `USE_EXTERNAL_STICKERS`, `CHANGE_NICKNAME`, `MANAGE_NICKNAMES`, `MENTION_EVERYONE`
* Added intents: `GUILD_MODERATION`, `GUILD_INVITES`
* Added new resource: `Sticker`
* New `Guild` endpoints:
    * `Guild.fetch_sticker`
    * `Guild.fetch_stickers`
    * `Guild.create_sticker`
    * `Guild.edit_sticker`
    * `Guild.delete_sticker`
    -- with the exception of a few endpoints, this completes the `Guild` resource
* New part: `ImageAssetPart` - currently only used for creating guild stickers

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

## [0.15.0] - Jan 2026

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

## [0.14.0] - Jan 2026

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

## [0.12.0] - Dec 2025

### Changed

* Added: `resolved` field to interaction data for efficient access to resolved objects
    * No API calls needed for USER/ROLE/CHANNEL command options
    * Attachment options now fully supported

* Clarified `ApplicationCommandOptionData.value` type annotation and added conversion guidance

* Bug fix: Boolean conversion in DataModel (string "false" now correctly converts to False)

## [0.11.0] - Dec 2025

### Breaking Changes

User was patched to be more bot specific. Some endpoints are not accessible to bots.

* `User.fetch_guilds` endpoint is no longer a method
    * this is a user endpoint and ScurryPy does not support User tokens

### Changes

* Bug fix: `User.fetch_guild_member` endpoint corrected

## [0.10.1] - Dec 2025

### Changes

Logging has been improved for finer grained control.

* Gateway heartbeat logs are now emitted at `DEBUG` level.

## [0.10.0] - Dec 2025

### Changes

Logging has been improved for finer grained control.

* Events not registered by the user are now `DEBUG` messages.

## [0.9.0] - Dec 2025

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

## [0.8.8.2] - Dec 2025

### Changed
* Corrected `FileUpload`: `component: LabelChild` is supposed to be `custom_id: str`.
See [FileUpload](https://scurry-works.github.io/scurrypy/api/ui_components/#scurrypy.parts.components_v2.FileUpload) for the updated version.

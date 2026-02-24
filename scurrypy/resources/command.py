from dataclasses import dataclass
from typing import Unpack

from .base_resource import BaseResource

from ..core.snowflake import Snowflake
from ..core.serialization import serialize

from ..api.commands.application_command import ApplicationCommandModel
from ..api.commands.slash import SlashCommandPart
from ..api.commands.context import UserCommandPart, MessageCommandPart

from ..params.command import EditGlobalCommandParams, EditGuildCommandParams

@dataclass
class GlobalCommand(BaseResource):
    """Represents a global command."""

    application_id: Snowflake
    """Application ID of the commands."""

    async def fetch(self, command_id: Snowflake) -> ApplicationCommandModel:
        """Fetches a command object.

        Args:
            command_id (int): ID of the command to fetch

        Returns:
            (ApplicationCommandModel): queried application command
        """
        data = await self.http.request('GET', f"applications/{self.application_id}/commands/{command_id}")

        return ApplicationCommandModel.from_dict(data)
    
    async def fetch_all(self) -> list[ApplicationCommandModel]:
        """Fetches ALL global commands.

        Returns:
            (list[ApplicationCommandModel]): queried list of application commands
        """
        data = await self.http.request('GET', f"applications/{self.application_id}/commands")

        assert isinstance(data, list)
        return [ApplicationCommandModel.from_dict(cmd) for cmd in data]

    async def create(self, command: SlashCommandPart | UserCommandPart | MessageCommandPart) -> ApplicationCommandModel:
        """Add a command to the client.

        !!! danger
            Creating a command with the same name as an existing command in the same scope will overwrite the old command.

        Args:
            command (SlashCommandPart | UserCommandPart | MessageCommandPart): command to register

        Returns:
            (ApplicationCommandModel): created command
        """
        data = await self.http.request('POST', f"applications/{self.application_id}/commands", data=command.to_dict())

        return ApplicationCommandModel.from_dict(data)

    async def edit(self, command_id: Snowflake, **options: Unpack[EditGlobalCommandParams]) -> ApplicationCommandModel:
        """Edit a command.

        Args:
            command_id (Snowflake): ID of command to edit
            options (EditGlobalCommandParams): command fields to edit

        Returns:
            (ApplicationCommandModel): updated application command
        """
        opts = serialize(dict(options))

        data = await self.http.request('PATCH', f"applications/{self.application_id}/commands/{command_id}", data=opts)

        return ApplicationCommandModel.from_dict(data)

    async def delete(self, command_id: Snowflake) -> None:
        """Delete a command.

        Args:
            command_id (Snowflake): ID of the command to delete
        """
        await self.http.request('DELETE', f"applications/{self.application_id}/commands/{command_id}")

    async def bulk_overwrite(self, commands: list[SlashCommandPart | UserCommandPart | MessageCommandPart]) -> list[ApplicationCommandModel]:
        """Takes a list of application commands, overwriting existing commands list for this application. 
        
        !!! warning
            Commands that do not already exist will count toward daily application command create limits.

        !!! danger
            This will overwrite all types of application commands: slash commands, user commands, and message commands.

        Args:
            commands (list[SlashCommandPart | UserCommandPart | MessageCommandPart]): commands to register

        Returns:
            (list[ApplicationCommandModel]): created application commands
        """

        data = await self.http.request(
            'PUT', 
            f"applications/{self.application_id}/commands", 
            data=[cmd.to_dict() for cmd in commands]
        )

        assert isinstance(data, list)
        return [ApplicationCommandModel.from_dict(cmd) for cmd in data]


@dataclass
class GuildCommand(BaseResource):
    """Represents a guild command."""

    application_id: Snowflake
    """Application ID of the commands."""

    guild_id: Snowflake
    "Guild ID of command."

    async def fetch(self, command_id: Snowflake) -> ApplicationCommandModel:
        """Fetches the command object.

        Args:
            command_id (int): ID of command to fetch

        Returns:
            (ApplicationCommandModel): queried application command
        """
        data = await self.http.request('GET', f"applications/{self.application_id}/guilds/{self.guild_id}/commands/{command_id}")

        return ApplicationCommandModel.from_dict(data)
    
    async def fetch_all(self) -> list[ApplicationCommandModel]:
        """Fetches ALL guild commands.

        Returns:
            (list[ApplicationCommandModel]): queried list of application commands
        """
        data = await self.http.request('GET', f"applications/{self.application_id}/guilds/{self.guild_id}/commands" )

        assert isinstance(data, list)
        return [ApplicationCommandModel.from_dict(cmd) for cmd in data]

    async def create(self, command: SlashCommandPart | UserCommandPart | MessageCommandPart) -> ApplicationCommandModel:
        """Add a command to the client.

        !!! danger
            Creating a command with the same name as an existing command in the same scope will overwrite the old command.

        Args:
            command (SlashCommandPart | UserCommandPart | MessageCommandPart): command to register

        Returns:
            (ApplicationCommandModel): created command
        """
        data = await self.http.request('POST', f"applications/{self.application_id}/guilds/{self.guild_id}/commands", data=command.to_dict())

        return ApplicationCommandModel.from_dict(data)

    async def edit(self, command_id: Snowflake, **options: Unpack[EditGuildCommandParams]) -> ApplicationCommandModel:
        """Edit a command.

        Args:
            command_id (Snowflake): ID of command to edit
            options (EditGuildCommandParams): command fields to edit

        Returns:
            (ApplicationCommandModel): updated application command
        """
        opts = serialize(dict(options))
        
        data = await self.http.request(
            'PATCH', 
            f"applications/{self.application_id}/guilds/{self.guild_id}/commands/{command_id}", 
            data=opts
        )

        return ApplicationCommandModel.from_dict(data)

    async def delete(self, command_id: Snowflake) -> None:
        """Delete a command.

        Args:
            command_id (Snowflake): ID of command to delete
        """
        await self.http.request('DELETE', f"applications/{self.application_id}/guilds/{self.guild_id}/commands/{command_id}")

    async def bulk_overwrite(self, commands: list[SlashCommandPart | UserCommandPart | MessageCommandPart]) -> list[ApplicationCommandModel]:
        """Takes a list of application commands, overwriting existing commands list for this guild. 
        
        !!! warning
            Commands that do not already exist will count toward daily application command create limits.

        !!! danger
            This will overwrite all types of application commands: slash commands, user commands, and message commands.

        Args:
            commands (list[SlashCommandPart | UserCommandPart | MessageCommandPart]): commands to register

        Returns:
            (list[ApplicationCommandModel]): created application commands
        """
        data = await self.http.request(
            'PUT', 
            f"applications/{self.application_id}/guilds/{self.guild_id}/commands", 
            data=[cmd.to_dict() for cmd in commands]
        )

        assert isinstance(data, list)
        return [ApplicationCommandModel.from_dict(cmd) for cmd in data]

from dataclasses import dataclass
from typing import Optional, Unpack

from .base_resource import BaseResource

from ..models.command import ApplicationCommandModel

from ..parts.command import SlashCommandPart, UserCommandPart, MessageCommandPart

from ..params.command import EditGlobalCommandParams, EditGuildCommandParams

@dataclass
class Command(BaseResource):
    """Represents a Discord command."""

    application_id: int
    """Application ID of the commands."""

@dataclass
class GlobalCommand(Command):

    async def fetch(self, command_id: int) -> ApplicationCommandModel:
        """Fetches a command object.

        Returns:
            (ApplicationCommandModel): queried application command
        """
        data = await self._http.request('GET', f"applications/{self.application_id}/commands/{command_id}")

        return ApplicationCommandModel.from_dict(data)
    
    async def fetch_all(self) -> list[ApplicationCommandModel]:
        """Fetches ALL global commands.

        Returns:
            (list[ApplicationCommandModel]): queried list of application commands
        """
        data = await self._http.request('GET', f"applications/{self.application_id}/commands")

        return [ApplicationCommandModel.from_dict(cmd) for cmd in data]

    async def create(self, command: SlashCommandPart | UserCommandPart | MessageCommandPart) -> ApplicationCommandModel:
        """Add command to the client.

        !!! danger
            Creating a command with the same name as an existing command in the same scope will overwrite the old command.

        Args:
            command (SlashCommandPart | UserCommandPart | MessageCommandPart): command to register

        Returns:
            (ApplicationCommandModel): created command
        """
        data = await self._http.request('POST', f"applications/{self.application_id}/commands", data=command.to_dict())

        return ApplicationCommandModel.from_dict(data)

    async def edit(self, command_id: int, **options: Unpack[EditGlobalCommandParams]) -> ApplicationCommandModel:
        """Edit this command.

        Args:
            command_id (int): ID of command to edit
            options (EditGlobalCommandParams): command fields to edit

        Returns:
            (ApplicationCommandModel): updated application command
        """
        if not self.id:
            raise ValueError("No command ID to fetch.")
        
        if options.get('options'):
            options['options'] = [i.to_dict() for i in options['options']]

        data = await self._http.request('PATCH', f"applications/{self.application_id}/commands/{command_id}", data=options)

        return ApplicationCommandModel.from_dict(data)

    async def delete(self, command_id: int) -> None:
        """Delete a command.

        Args:
            command_id (int): ID of the command to delete
        """
        await self._http.request('DELETE', f"applications/{self.application_id}/commands/{command_id}")

    async def bulk_overwrite(self, commands: list[SlashCommandPart | UserCommandPart | MessageCommandPart]) -> list[ApplicationCommandModel]:
        """Takes a list of application commands, overwriting the existing global command list for this application. 
        
        !!! warning
            Commands that do not already exist will count toward daily application command create limits.

        !!! danger
            This will overwrite all types of application commands: slash commands, user commands, and message commands.

        Args:
            commands (list[SlashCommandPart | UserCommandPart | MessageCommandPart]): commands to register

        Returns:
            (list[ApplicationCommandModel]): created application commands
        """

        data = await self._http.request(
            'PUT', 
            f"applications/{self.application_id}/commands", 
            data=[cmd.to_dict() for cmd in commands]
        )

        return [ApplicationCommandModel.from_dict(cmd) for cmd in data]


@dataclass
class GuildCommand(Command):
    """Represents a guild command."""

    guild_id: Optional[int]
    "Guild ID of command."

    async def fetch(self, command_id: int) -> ApplicationCommandModel:
        """Fetches the command object.

        Args:
            command_id (int): ID of command to fetch

        Returns:
            (ApplicationCommandModel): queried application command
        """
        data = await self._http.request('GET', f"applications/{self.application_id}/guilds/{self.guild_id}/commands/{command_id}")

        return ApplicationCommandModel.from_dict(data)
    
    async def fetch_all(self) -> list[ApplicationCommandModel]:
        """Fetches ALL guild commands.

        Returns:
            (list[ApplicationCommandModel]): queried list of application commands
        """
        data = await self._http.request('GET', f"applications/{self.application_id}/guilds/{self.guild_id}/commands" )

        return [ApplicationCommandModel.from_dict(cmd) for cmd in data]

    async def create(self, command: SlashCommandPart | UserCommandPart | MessageCommandPart) -> ApplicationCommandModel:
        """Add command to the client.

        !!! danger
            Creating a command with the same name as an existing command in the same scope will overwrite the old command.

        Args:
            command (SlashCommandPart | UserCommandPart | MessageCommandPart): command to register

        Returns:
            (ApplicationCommandModel): created command
        """
        data = await self._http.request('POST', f"applications/{self.application_id}/guilds/{self.guild_id}/commands", data=command.to_dict())

        return ApplicationCommandModel.from_dict(data)

    async def edit(self, command_id: int, **options: Unpack[EditGuildCommandParams]) -> ApplicationCommandModel:
        """Edit a command.

        Args:
            command_id (int): ID of command to edit
            options (EditGuildCommandParams): command fields to edit

        Returns:
            (ApplicationCommandModel): updated application command
        """
        if options.get('options'):
            options['options'] = [i.to_dict() for i in options['options']]

        data = await self._http.request(
            'PATCH', 
            f"applications/{self.application_id}/guilds/{self.guild_id}/commands/{command_id}", 
            data=options
        )

        return ApplicationCommandModel.from_dict(data)

    async def delete(self, command_id: int) -> None:
        """Delete a command.

        Args:
            command_id (int): ID of command to delete
        """
        await self._http.request('DELETE', f"applications/{self.application_id}/guilds/{self.guild_id}/commands/{command_id}")

    async def bulk_overwrite(self, commands: list[SlashCommandPart | UserCommandPart | MessageCommandPart]) -> list[ApplicationCommandModel]:
        """Takes a list of application commands, overwriting the existing global or guild command list for this application. 
        
        !!! warning
            Commands that do not already exist will count toward daily application command create limits.

        !!! danger
            This will overwrite all types of application commands: slash commands, user commands, and message commands.

        Args:
            commands (list[SlashCommandPart | UserCommandPart | MessageCommandPart]): commands to register

        Returns:
            (list[ApplicationCommandModel]): created application commands
        """
        data = await self._http.request(
            'PUT', 
            f"applications/{self.application_id}/guilds/{self.guild_id}/commands", 
            data=[cmd.to_dict() for cmd in commands]
        )

        return [ApplicationCommandModel.from_dict(cmd) for cmd in data]

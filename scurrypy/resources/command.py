from dataclasses import dataclass
from typing import Optional, Unpack

from .base_resource import BaseResource

from ..models.command import ApplicationCommandModel

from ..parts.command import SlashCommand, UserCommand, MessageCommand

from ..params.command import EditGlobalCommandParams, EditGuildCommandParams

@dataclass
class Command(BaseResource):
    """Represents a Discord command."""

    application_id: int
    """Application ID of the commands."""

    id: int = None
    """ID of the command."""

@dataclass
class GlobalCommand(Command):

    async def fetch(self) -> ApplicationCommandModel:
        """Fetches the command object.

        Raises:
            (ValueError): no ID set

        Returns:
            (ApplicationCommandModel): queried application command
        """
        if not self.id:
            raise ValueError("No command ID to fetch.")
        
        data = await self._http.request('GET', f"applications/{self.application_id}/commands/{self.id}")

        return ApplicationCommandModel.from_dict(data)
    
    async def fetch_all(self) -> list[ApplicationCommandModel]:
        """Fetches ALL global commands.

        Returns:
            (list[ApplicationCommandModel]): queried list of application commands
        """
        data = await self._http.request('GET', f"applications/{self.application_id}/commands")

        return [ApplicationCommandModel.from_dict(cmd) for cmd in data]

    async def create(self, command: SlashCommand | UserCommand | MessageCommand) -> ApplicationCommandModel:
        """Add command to the client.

        !!! danger
            Creating a command with the same name as an existing command in the same scope will overwrite the old command.

        Args:
            command (SlashCommand | UserCommand | MessageCommand): command to register

        Returns:
            (ApplicationCommandModel): created command
        """
        data = await self._http.request('POST', f"applications/{self.application_id}/commands", data=command.to_dict())

        return ApplicationCommandModel.from_dict(data)

    async def edit(self, **options: Unpack[EditGlobalCommandParams]) -> ApplicationCommandModel:
        """Edit this command.

        Args:
            options (EditGlobalCommandParams): command fields to edit
        
        Raises:
            (ValueError): no ID set

        Returns:
            (ApplicationCommandModel): updated application command
        """
        if not self.id:
            raise ValueError("No command ID to fetch.")
        
        if options.get('options'):
            options['options'] = [i.to_dict() for i in options['options']]

        data = await self._http.request('PATCH', f"applications/{self.application_id}/commands", data=options)

        return ApplicationCommandModel.from_dict(data)

    async def delete(self) -> None:
        """Delete this command.

        Raises:
            (ValueError): No ID set
        """
        if not self.id:
            raise ValueError("No command ID to fetch.")

        await self._http.request('DELETE', f"applications/{self.application_id}/commands")

    async def bulk_overwrite(self, commands: list[SlashCommand | UserCommand | MessageCommand]) -> list[ApplicationCommandModel]:
        """Takes a list of application commands, overwriting the existing global command list for this application. 
        
        !!! warning
            Commands that do not already exist will count toward daily application command create limits.

        !!! danger
            This will overwrite all types of application commands: slash commands, user commands, and message commands.

        Args:
            commands (list[SlashCommand  |  UserCommand  |  MessageCommand]): commands to register

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

    guild_id: Optional[int] = None
    "Guild ID of command."

    async def fetch(self) -> ApplicationCommandModel:
        """Fetches the command object.

        Raises:
            (ValueError): no ID set

        Returns:
            (ApplicationCommandModel): queried application command
        """
        if not self.id:
            raise ValueError("No command ID to fetch.")
        
        data = await self._http.request('GET', f"applications/{self.application_id}/guilds/{self.guild_id}/commands/{self.id}")

        return ApplicationCommandModel.from_dict(data)
    
    async def fetch_all(self) -> list[ApplicationCommandModel]:
        """Fetches ALL guild commands.

        Returns:
            (list[ApplicationCommandModel]): queried list of application commands
        """
        data = await self._http.request('GET', f"applications/{self.application_id}/guilds/{self.guild_id}/commands" )

        return [ApplicationCommandModel.from_dict(cmd) for cmd in data]

    async def create(self, command: SlashCommand | UserCommand | MessageCommand) -> ApplicationCommandModel:
        """Add command to the client.

        !!! danger
            Creating a command with the same name as an existing command in the same scope will overwrite the old command.

        Args:
            command (SlashCommand | UserCommand | MessageCommand): command to register

        Returns:
            (ApplicationCommandModel): created command
        """
        data = await self._http.request('POST', f"applications/{self.application_id}/guilds/{self.guild_id}/commands", data=command.to_dict())

        return ApplicationCommandModel.from_dict(data)

    async def edit(self, **options: Unpack[EditGuildCommandParams]) -> ApplicationCommandModel:
        """Edit a command.

        Args:
            options (EditGuildCommandParams): command fields to edit
        
        Raises:
            (ValueError): no ID set

        Returns:
            (ApplicationCommandModel): updated application command
        """
        if not self.id:
            raise ValueError("No command ID to fetch.")
        
        if options.get('options'):
            options['options'] = [i.to_dict() for i in options['options']]

        data = await self._http.request(
            'PATCH', 
            f"applications/{self.application_id}/guilds/{self.guild_id}/commands/{self.id}", 
            data=options
        )

        return ApplicationCommandModel.from_dict(data)

    async def delete(self) -> None:
        """Delete this command.

        Raises:
            (ValueError): No ID set
        """
        if not self.id:
            raise ValueError("No command ID to fetch.")

        await self._http.request('DELETE', f"applications/{self.application_id}/guilds/{self.guild_id}/commands/{self.id}")

    async def bulk_overwrite(self, commands: list[SlashCommand | UserCommand | MessageCommand]) -> list[ApplicationCommandModel]:
        """Takes a list of application commands, overwriting the existing global or guild command list for this application. 
        
        !!! warning
            Commands that do not already exist will count toward daily application command create limits.

        !!! danger
            This will overwrite all types of application commands: slash commands, user commands, and message commands.

        Args:
            commands (list[SlashCommand  |  UserCommand  |  MessageCommand]): commands to register

        Returns:
            (list[ApplicationCommandModel]): created application commands
        """
        data = await self._http.request(
            'PUT', 
            f"applications/{self.application_id}/guilds/{self.guild_id}/commands", 
            data=[cmd.to_dict() for cmd in commands]
        )

        return [ApplicationCommandModel.from_dict(cmd) for cmd in data]

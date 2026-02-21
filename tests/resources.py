from scurrypy import Client

client = Client(token='...')

from scurrypy.resources import Application
application = client.application(123)
assert isinstance(application, Application)
assert application.id == 123

from scurrypy.resources import ApplicationEmoji
app_emoji = client.application_emoji(123)
assert isinstance(app_emoji, ApplicationEmoji)
assert app_emoji.application_id == 123

from scurrypy.resources import GuildEmoji
guild_emoji = client.guild_emoji(123)
assert isinstance(guild_emoji, GuildEmoji)
assert guild_emoji.guild_id == 123

from scurrypy.resources import Guild
guild = client.guild(123)
assert isinstance(guild, Guild)
assert guild.id == 123

from scurrypy.resources import Channel
channel = client.channel(123)
assert isinstance(channel, Channel)
assert channel.id == 123

from scurrypy.resources import Invite
invite = client.invite('abc123')
assert isinstance(invite, Invite)
assert invite.code == 'abc123'

from scurrypy.resources import GlobalCommand
global_cmd = client.global_command(123)
assert isinstance(global_cmd, GlobalCommand)
assert global_cmd.application_id == 123

from scurrypy.resources import GuildCommand
guild_cmd = client.guild_command(123, 456)
assert isinstance(guild_cmd, GuildCommand)
assert guild_cmd.application_id == 123
assert guild_cmd.guild_id == 456

from scurrypy.resources import Message
msg = client.message(123, 456)
assert isinstance(msg, Message)
assert msg.channel_id == 123
assert msg.id == 456

from scurrypy.resources import Interaction
interaction = client.interaction(123, 'abc123')
assert isinstance(interaction, Interaction)
assert interaction.id == 123
assert interaction.token == 'abc123'

from scurrypy.resources import Sticker
sticker = client.sticker()
assert isinstance(sticker, Sticker)

from scurrypy.resources import User
user = client.user()
assert isinstance(user, User)

from syncord.config import settings
from syncord.discord_bot import bot as discord_bot

settings.SYNC_COMMANDS = True
discord_bot.run(settings.DISCORD_TOKEN)

from keep_alive import keep_alive
from syncord.config import settings
from syncord.discord_bot import bot as discord_bot


# keep_alive()
discord_bot.run(settings.DISCORD_TOKEN)

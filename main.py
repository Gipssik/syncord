import asyncio

from syncord.config import settings
from syncord.discord_bot import bot as discord_bot
from syncord.telegram_bot import dispatcher as telegram_dispatcher, bot as telegram_bot


async def discord_runner():
    async with discord_bot:
        await discord_bot.start(settings.DISCORD_TOKEN)


async def main():
    coros = [
        discord_runner(),
        telegram_dispatcher.start_polling(telegram_bot),
    ]
    await asyncio.gather(*coros)


if __name__ == "__main__":
    asyncio.run(main())

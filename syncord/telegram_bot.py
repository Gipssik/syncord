from aiogram import Bot

from syncord.config import settings

telegram_bot = Bot(token=settings.TELEGRAM_TOKEN)


async def ping_missing_members(missing_members: list[str], tg_chat_id: int, author: str, dynamic_message: str = None):
    if not missing_members:
        return
    if dynamic_message is None:
        dynamic_message = "Заходьте в дискорд"
    message = f'{dynamic_message}: {", ".join([f"@{member}" for member in missing_members])}\n(Автор: {author})'
    await telegram_bot.send_message(chat_id=tg_chat_id, text=message)


async def send_message(message: str, tg_chat_id: int):
    await telegram_bot.send_message(chat_id=tg_chat_id, text=message)

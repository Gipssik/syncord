from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.formatting import BotCommand

from syncord.config import settings

bot = Bot(token=settings.TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dispatcher = Dispatcher()


async def send_message(message: str, tg_chat_id: int):
    await bot.send_message(chat_id=tg_chat_id, text=message)


async def ping_missing_members(missing_members: list[str], tg_chat_id: int, author: str, dynamic_message: str = None):
    if not missing_members:
        return
    if dynamic_message is None:
        dynamic_message = "Заходьте в дискорд"
    message = f'{dynamic_message}: {", ".join([f"@{member}" for member in missing_members])}\n\n(від: {author})'
    await send_message(message, tg_chat_id)


@dispatcher.startup()
async def startup():
    print("Telegram bot started")


@dispatcher.message(CommandStart())
async def command_start(message: Message) -> None:
    message_text = (
        f"Привіт, я буду синхронізувати вас з дискордом!\n\n"
        f"Будь ласка, додайте дискорд-бота до свого телеграм-чату і напишіть команду {BotCommand('/start')}"
    )

    await send_message(message_text, message.chat.id)


@dispatcher.message(Command("chat_id"))
async def command_start_group(message: Message) -> None:
    if message.chat.type not in ("group", "supergroup"):
        return
    message_text = (
        f"<b>Ваш chat_id:</b> <code>{message.chat.id}</code>.\n\n"
        f"Будь ласка, додайте дискорд-бота до своєї гільдії і зареєструйте там це айді."
    )

    await send_message(message_text, message.chat.id)

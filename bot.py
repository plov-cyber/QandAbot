"""File with telegram-bot. Creates, initializes and starts the bot."""

# Libraries, classes and functions imports
import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from callbacks.common_callbacks import register_cb_query_handlers
from config import TOKEN
from handlers.common_handlers import register_common_handlers
from handlers.quiz_handlers import register_quiz_handlers

# Creating bot and dispatcher
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Handlers and callbacks registration
register_common_handlers(dp)
register_cb_query_handlers(dp)
register_quiz_handlers(dp)


async def shutdown(dp: Dispatcher):
    """Function for bot shutdown."""

    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)

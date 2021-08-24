"""File with telegram-bot. Creates, initializes and starts the bot."""

# Libraries, classes and functions imports
import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from callbacks.common_callbacks import register_cb_query_handlers
from config import TOKEN
from handlers.ask_question_handlers import register_ask_question_handlers
from handlers.common_handlers import register_common_handlers
from handlers.common_user_handlers import register_common_user_handlers
from handlers.find_question_handlers import register_find_question_handlers
from handlers.quiz_handlers import register_quiz_handlers
from handlers.respondent_handlers import register_respondent_handlers

# Creating bot, logger and dispatcher
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
logger = logging.getLogger(__name__)

# Handlers and callbacks registration
register_common_handlers(dp)
register_cb_query_handlers(dp)
register_quiz_handlers(dp)
register_respondent_handlers(dp)
register_common_user_handlers(dp)
register_find_question_handlers(dp)
register_ask_question_handlers(dp)


async def shutdown(dp: Dispatcher):
    """Function for bot shutdown."""

    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)

"""File with telegram-bot. Creates, initializes and starts the bot."""

# Initializing database
from data import db_session

db_session.global_init('db/data.sqlite')

# Libraries, classes and functions imports
import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from callbacks.common_callbacks import register_common_callbacks
from callbacks.find_question_callbacks import register_find_question_callbacks
from config import TOKEN
from handlers.ask_question_handlers import register_ask_question_handlers
from handlers.common_handlers import register_common_handlers
from handlers.common_user_handlers import register_common_user_handlers
from handlers.find_question_handlers import register_find_question_handlers
from handlers.quiz_handlers import register_quiz_handlers
from handlers.respondent_handlers import register_respondent_handlers
from callbacks.respondent_callbacks import register_respondent_callbacks
from handlers.dialogue_handlers import register_dialogue_handlers
from callbacks.dialogue_callbacks import register_dialogue_callbacks

# Creating bot, logger and dispatcher
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
logger = logging.getLogger(__name__)

# Handlers and callbacks registration
register_common_handlers(dp)
register_quiz_handlers(dp)
register_respondent_handlers(dp)
register_common_user_handlers(dp)
register_find_question_handlers(dp)
register_ask_question_handlers(dp)
register_dialogue_handlers(dp)

register_dialogue_callbacks(dp)
register_common_callbacks(dp)
register_find_question_callbacks(dp)
register_respondent_callbacks(dp)


async def shutdown(dp: Dispatcher):
    """Function for bot shutdown."""

    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)

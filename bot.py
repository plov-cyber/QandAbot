import logging
import os

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from callbacks.common import register_cb_query_handlers
from config import TOKEN
from handlers.common import register_common_handlers
from handlers.questions import register_question_handlers
from handlers.quiz import register_quiz_handlers

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

register_common_handlers(dp)
register_question_handlers(dp)
register_cb_query_handlers(dp)
register_quiz_handlers(dp)


async def shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)

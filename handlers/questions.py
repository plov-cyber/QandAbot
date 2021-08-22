from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from handlers.states import wait_for_question, find_question


async def send_the_test(message: types.Message):
    pass


def register_question_handlers(dp: Dispatcher):
    pass

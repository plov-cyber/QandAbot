"""Find question callbacks."""

# imports
import logging

from aiogram import types, Dispatcher
from handlers.find_question_handlers import user_data

logger = logging.getLogger(__name__)


async def swipe_question(callback: types.CallbackQuery):
    """Callback for swiping questions."""

    i, questions = user_data.get(callback.from_user.id)
    size = len(questions)
    action = callback.data
    if action == "previous_question":
        user_data[callback.from_user.id][0] = (i - 1 + size) % size
        await callback.message.edit_text(text=f"{questions[i].text}")
        await callback.answer()
    elif action == "next_question":
        user_data[callback.from_user.id][0] = (i + 1) % size
        await callback.message.edit_text(text=f"{questions[i].text}")
        await callback.answer()


def register_find_question_callbacks(dp: Dispatcher):
    """Registers all common callbacks to dispatcher."""

    logger.info(msg="Registering common callbacks.")
    dp.register_callback_query_handler(swipe_question)

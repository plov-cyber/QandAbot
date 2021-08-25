"""Find question callbacks."""

# imports
import logging

from aiogram import types, Dispatcher

from handlers.find_question_handlers import user_data, showing_questions_keyboard
from handlers.states import FindQuestionStates

logger = logging.getLogger(__name__)


async def swipe_question(callback: types.CallbackQuery):
    """Callback for swiping questions."""

    i, questions = user_data.get(callback.from_user.id)
    size = len(questions)
    action = callback.data
    if action == "previous_question":
        i = (i - 1 + size) % size
        buttons = [
            [types.InlineKeyboardButton(text='<--', callback_data="previous_question"),
             types.InlineKeyboardButton(text=f'{i + 1}/{size}', callback_data="question_num"),
             types.InlineKeyboardButton(text='-->', callback_data="next_question")],
            [types.InlineKeyboardButton(text='Show answer',  callback_data="show_answer")]
        ]
        showing_questions_keyboard.inline_keyboard = buttons
        await callback.message.edit_text(text=f"{questions[i].text}",
                                         reply_markup=showing_questions_keyboard)
    elif action == "next_question":
        i = (i + 1) % size
        buttons = [
            [types.InlineKeyboardButton(text='<--', callback_data="previous_question"),
             types.InlineKeyboardButton(text=f'{i + 1}/{size}', callback_data="question_num"),
             types.InlineKeyboardButton(text='-->', callback_data="next_question")],
            [types.InlineKeyboardButton(text='Show answer', callback_data="show_answer")]
        ]
        showing_questions_keyboard.inline_keyboard = buttons
        await callback.message.edit_text(text=f"{questions[i].text}",
                                         reply_markup=showing_questions_keyboard)
    user_data[callback.from_user.id] = (i, questions)
    await callback.answer()


def register_find_question_callbacks(dp: Dispatcher):
    """Registers all common callbacks to dispatcher."""

    logger.info(msg="Registering common callbacks.")
    dp.register_callback_query_handler(swipe_question, state=FindQuestionStates.getting_hashtags)

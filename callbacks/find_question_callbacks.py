"""Find question callbacks."""

# imports
import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from handlers.find_question_handlers import is_answered_signs
from handlers.states import FindQuestionStates

logger = logging.getLogger(__name__)


async def swipe_found_question(callback: types.CallbackQuery, state: FSMContext):
    """Callback for swiping found questions."""

    user_data = await state.get_data()
    i, questions = user_data['index'], user_data['questions']
    showing_questions_keyboard = types.InlineKeyboardMarkup(row_width=3)
    size = len(questions)
    action = callback.data
    if size == 1:
        await callback.answer()
        return
    if action == "previous_question":
        i = (i - 1 + size) % size
    elif action == "next_question":
        i = (i + 1) % size
    buttons = [
        [types.InlineKeyboardButton(text='<--', callback_data="previous_question"),
         types.InlineKeyboardButton(text=f'{i + 1}/{size}', callback_data="question_num"),
         types.InlineKeyboardButton(text='-->', callback_data="next_question")]
    ]
    if questions[i].is_answered:
        buttons.append([types.InlineKeyboardButton(text='Show answer', callback_data="show_answer")])
    showing_questions_keyboard.inline_keyboard = buttons
    await state.update_data(index=i)
    await callback.message.edit_text(text=f"Question:\n"
                                          f"{questions[i].text}\n"
                                          f"Answered: {is_answered_signs[questions[i].is_answered]}",
                                     reply_markup=showing_questions_keyboard)
    await callback.answer()


def register_find_question_callbacks(dp: Dispatcher):
    """Registers all common callbacks to dispatcher."""

    logger.info(msg="Registering common callbacks.")
    dp.register_callback_query_handler(swipe_found_question, state=FindQuestionStates.show_questions)

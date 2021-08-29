"""Respondent callbacks."""

# imports
import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from handlers.states import RespondentStates

logger = logging.getLogger(__name__)


async def respondent_swipe_available_questions(callback: types.CallbackQuery, state: FSMContext):
    """Callback to swipe available questions."""

    user_data = await state.get_data()
    i, questions = user_data['index'], user_data['questions']
    available_questions_keyboard = types.InlineKeyboardMarkup(row_width=3)
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
         types.InlineKeyboardButton(text='-->', callback_data="next_question")],
        [types.InlineKeyboardButton(text='Give answer', callback_data='give_answer')]
    ]
    available_questions_keyboard.inline_keyboard = buttons
    await state.update_data(index=i)
    await callback.message.edit_text(text=f"Question:\n"
                                          f"{questions[i].text}\n",
                                     reply_markup=available_questions_keyboard)
    await callback.answer()


def register_respondent_callbacks(dp: Dispatcher):
    """Register all respondent callbacks to dispatcher."""

    logger.info(msg="Registering respondent callbacks.")
    dp.register_callback_query_handler(respondent_swipe_available_questions,
                                       state=RespondentStates.show_available_questions)

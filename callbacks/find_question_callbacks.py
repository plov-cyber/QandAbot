"""Find question callbacks."""

# imports
import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from data import db_session
from data.AnswerModel import Answer
from handlers.common_handlers import send_user_to_main_menu
from handlers.find_question_handlers import is_answered_signs
from handlers.states import FindQuestionStates, CommonStates

logger = logging.getLogger(__name__)
session = db_session.create_session()


async def swipe_found_question(callback: types.CallbackQuery, state: FSMContext):
    """Callback for swiping found questions."""

    user_data = await state.get_data()
    i, questions = user_data['index'], user_data['questions']
    message = user_data['message']
    show_answer = user_data['show_answer']
    showing_questions_keyboard = types.InlineKeyboardMarkup(row_width=3)
    size = len(questions)
    action = callback.data
    if action == "previous_question":
        i = (i - 1 + size) % size
    elif action == "next_question":
        i = (i + 1) % size
    elif action == "go_back":
        await CommonStates.to_main_menu.set()
        await callback.answer()
        await send_user_to_main_menu(message, state)
    elif action == 'show_answer':
        show_answer = True
    elif action == 'hide_answer':
        show_answer = False
    buttons = [
        [types.InlineKeyboardButton(text='⬅️', callback_data="previous_question"),
         types.InlineKeyboardButton(text=f'{i + 1}/{size}', callback_data="question_num"),
         types.InlineKeyboardButton(text='➡️', callback_data="next_question")]
    ]
    if questions[i].is_answered and not show_answer:
        buttons.append([types.InlineKeyboardButton(text='Show answer', callback_data="show_answer")])
    elif questions[i].is_answered and show_answer:
        buttons.append([types.InlineKeyboardButton(text='Hide answer', callback_data="hide_answer")])
    buttons.append([types.InlineKeyboardButton(text="Back to menu ↩️🥺", callback_data="go_back")])
    showing_questions_keyboard.inline_keyboard = buttons
    await state.update_data(index=i, show_answer=show_answer)
    if not show_answer:
        await callback.message.edit_text(text=f"Question:\n"
                                              f"{questions[i].text}\n\n"
                                              f"Answered: {is_answered_signs[questions[i].is_answered]}",
                                         reply_markup=showing_questions_keyboard)
    elif show_answer:
        answer = session.query(Answer).filter(Answer.question == questions[i]).first()
        await callback.message.edit_text(text=f"Question:\n"
                                              f"{questions[i].text}\n\n"
                                              f"Answer:\n"
                                              f"{answer.text}\n\n"
                                              f"Answered by: citizen #{answer.from_user_id % 1000} "
                                              f"⭐️{answer.from_user.rating}",
                                         reply_markup=showing_questions_keyboard)
    await callback.answer()


def register_find_question_callbacks(dp: Dispatcher):
    """Registers all common callbacks to dispatcher."""

    logger.info(msg="Registering common callbacks.")
    dp.register_callback_query_handler(swipe_found_question, state=FindQuestionStates.show_questions)

"""Respondent callbacks."""

# imports
import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from data import db_session
from data.QuestionModel import Question
from handlers.respondent_handlers import respondent_send_interactions
from handlers.states import RespondentStates

logger = logging.getLogger(__name__)
session = db_session.create_session()


async def respondent_swipe_available_questions(callback: types.CallbackQuery, state: FSMContext):
    """Callback to swipe available questions."""

    user_data = await state.get_data()
    i, questions = user_data['index'], user_data['questions']
    message = user_data['message']
    available_questions_keyboard = types.InlineKeyboardMarkup(row_width=3)
    size = len(questions)
    action = callback.data
    if action == "previous_question":
        i = (i - 1 + size) % size
    elif action == "next_question":
        i = (i + 1) % size
    elif action == 'go_back':
        await RespondentStates.send_interactions.set()
        await callback.answer()
        await respondent_send_interactions(message)
        return
    elif action == "give_answer":
        await state.reset_data()
        await state.update_data(question=questions[i])
        await callback.message.answer(text="Please write full and correct answer on given question:")
        await RespondentStates.give_answer.set()
    if size == 1:
        await callback.answer()
        return
    buttons = [
        [types.InlineKeyboardButton(text='⬅️', callback_data="previous_question"),
         types.InlineKeyboardButton(text=f'{i + 1}/{size}', callback_data="question_num"),
         types.InlineKeyboardButton(text='➡️', callback_data="next_question")],
        [types.InlineKeyboardButton(text='Give answer', callback_data='give_answer')],
        [types.InlineKeyboardButton(text="Back to menu ↩️🥺", callback_data='go_back')]
    ]
    available_questions_keyboard.inline_keyboard = buttons
    await state.update_data(index=i)
    await callback.message.edit_text(text=f"Question:\n"
                                          f"{questions[i].text}",
                                     reply_markup=available_questions_keyboard)
    await callback.answer()


async def respondent_swipe_answers(callback: types.CallbackQuery, state: FSMContext):
    """Callback to swipe answers."""

    user_data = await state.get_data()
    i, answers = user_data['index'], user_data['answers']
    message = user_data['message']
    show_answers_keyboard = types.InlineKeyboardMarkup(row_width=3)
    size = len(answers)
    action = callback.data
    if action == "previous_question":
        i = (i - 1 + size) % size
    elif action == "next_question":
        i = (i + 1) % size
    elif action == 'go_back':
        await RespondentStates.send_interactions.set()
        await respondent_send_interactions(message)
    buttons = [
        [types.InlineKeyboardButton(text='⬅️', callback_data="previous_question"),
         types.InlineKeyboardButton(text=f'{i + 1}/{size}', callback_data="question_num"),
         types.InlineKeyboardButton(text='➡️', callback_data="next_question")],
        [types.InlineKeyboardButton(text="Back to menu ↩️🥺", callback_data='go_back')]
    ]
    show_answers_keyboard.inline_keyboard = buttons
    await state.update_data(index=i)
    question = session.query(Question).filter(Question.id == answers[i].question_id).first()
    await callback.message.edit_text(text=f"Question:\n"
                                          f"{question.text}\n\n"
                                          f"Your answer:\n"
                                          f"{answers[i].text}",
                                     reply_markup=show_answers_keyboard)
    await callback.answer()


def register_respondent_callbacks(dp: Dispatcher):
    """Register all respondent callbacks to dispatcher."""

    logger.info(msg="Registering respondent callbacks.")
    dp.register_callback_query_handler(respondent_swipe_available_questions,
                                       state=RespondentStates.show_available_questions)
    dp.register_callback_query_handler(respondent_swipe_answers, state=RespondentStates.show_answers)

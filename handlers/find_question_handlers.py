"""Handlers for finding questions."""

# Libraries, classes and functions imports
import logging

from aiogram import types, Dispatcher

from data import db_session
from data.QuestionModel import Question
from handlers.states import FindQuestionStates

logger = logging.getLogger(__name__)

user_data = {}


async def get_hashtags(message: types.Message):
    """Gets hashtags from user and finds questions."""

    logger.info(msg=f"Getting hashtags from user {message.from_user.first_name}(@{message.from_user.username}).")
    hashtags = message.text
    if hashtags[0] != '#':
        await message.answer(text="Please write hashtags like this: #hashtag1#hashtag2...")
        return

    hashtags = hashtags[1:].lower().split('#')

    session = db_session.create_session()
    questions = session.query(Question).all()
    suit_questions = []
    for q in questions:
        q_hashs = [h.text for h in q.hashtags]
        suit_hashtags = list(set(q_hashs) & set(hashtags))
        if suit_hashtags:
            suit_questions.append((q, len(suit_hashtags)))
    suit_questions = list(map(lambda x: x[0], sorted(suit_questions, key=lambda x: x[1])))  # list of questions
    user_data[message.from_user.id] = (0, suit_questions)

    buttons = [
        types.InlineKeyboardButton(text='<--', callback_data="previous_question"),
        types.InlineKeyboardButton(text='-->', callback_data="next_question"),
        types.InlineKeyboardButton(text='Show answers', callback_data="")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await message.answer(text=f"{suit_questions[0]}")


def register_find_question_handlers(dp: Dispatcher):
    """Registers all find_question_handler to dispatcher."""

    logger.info(msg=f"Registering find_question handlers.")
    dp.register_message_handler(get_hashtags, state=FindQuestionStates.getting_hashtags)

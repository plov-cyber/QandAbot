"""Handlers for finding questions."""

# Libraries, classes and functions imports
import logging

from aiogram import types, Dispatcher

from data import db_session
from data.QuestionModel import Question
from handlers.states import FindQuestionStates

logger = logging.getLogger(__name__)


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
    suit_questions.sort(key=lambda x: x[1], reverse=True)



def register_find_question_handlers(dp: Dispatcher):
    """Registers all find_question_handler to dispatcher."""

    dp.register_message_handler(get_hashtags, state=FindQuestionStates.getting_hashtags)

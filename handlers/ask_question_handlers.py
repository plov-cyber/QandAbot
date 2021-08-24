"""Handlers for asking questions."""

# Libraries, classes and functions imports
import logging

from aiogram import types, Dispatcher

from handlers.states import AskQuestionStates

logger = logging.getLogger(__name__)


async def get_question(message: types.Message):
    """Gets question from user."""

    logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) asking a question.")
    question = message.text


def register_ask_question_handlers(dp: Dispatcher):
    """Registers all ask_question_handlers to dispatcher."""

    logger.info(msg="Registering ask_question handlers.")
    dp.register_message_handler(get_question, state=AskQuestionStates.getting_question)

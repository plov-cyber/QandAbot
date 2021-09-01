"""Dialogue callbacks."""

# imports
import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from data import db_session
from data.QuestionModel import Question
from handlers.dialogue_handlers import data
from handlers.states import DialogueStates

logger = logging.getLogger(__name__)
session = db_session.create_session()


async def redirect_to_chat(callback: types.CallbackQuery, state: FSMContext):
    """Redirects user to chat."""

    await DialogueStates.chatting.set()
    user_data = data[callback.from_user.id]
    request = user_data['request']
    question = session.query(Question).get(request.question_id)
    await callback.message.answer(text=f"You're in anonymous chat about question:\n"
                                       f"{question.text}\"\n")
    await callback.bot.send_message(chat_id=request.to_user_id, text="Your talker is here. Start chatting!")
    await callback.answer()


def register_dialogue_callbacks(dp: Dispatcher):
    """Registers all dialogue callbacks to dispatcher."""

    dp.register_callback_query_handler(redirect_to_chat, Text(equals="start_chat"), state="*")

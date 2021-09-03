"""Dialogue callbacks."""

# imports
import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

from data import db_session
from data.QuestionModel import Question
from data.UserModel import User
from handlers.dialogue_handlers import data, leave_chat_kb
from handlers.states import DialogueStates

logger = logging.getLogger(__name__)
session = db_session.create_session()


async def redirect_to_chat(callback: types.CallbackQuery):
    """Redirects user to chat."""

    await DialogueStates.chatting.set()
    user_data = data[callback.from_user.id]
    request = user_data['request']
    question = session.query(Question).get(request.question_id)
    data[request.from_user_id] = {}
    data[request.from_user_id]['request'] = request
    respondent = session.query(User).get(request.to_user_id)
    user = session.query(User).get(request.from_user_id)
    await callback.message.answer(text=f"You're in anonymous chat about question:\n"
                                       f"{question.text}\"\n", reply_markup=leave_chat_kb)
    await callback.bot.send_message(chat_id=request.to_user_id, text="Your talker is here. Start chatting!")
    logger.info(msg=f"User {user.first_name}(@{user.username}) and"
                    f" respondent {respondent.first_name}(@{respondent.username}) started anonymous chat.")
    await callback.answer()


def register_dialogue_callbacks(dp: Dispatcher):
    """Registers all dialogue callbacks to dispatcher."""

    dp.register_callback_query_handler(redirect_to_chat, Text(equals="start_chat"), state="*")

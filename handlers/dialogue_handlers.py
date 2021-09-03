"""Dialogue handlers."""

# imports
import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from data import db_session
from data.QuestionModel import Question
from handlers.common_handlers import send_user_to_main_menu
from handlers.states import DialogueStates, CommonStates

logger = logging.getLogger(__name__)
session = db_session.create_session()

data = {}
leave_chat_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
leave_chat_kb.add(types.KeyboardButton(text="Leave chat"))


async def start_chat(message: types.Message, state: FSMContext):
    """Starts anonymous chat."""

    user_data = await state.get_data()
    request = user_data['request']
    data[request.from_user_id] = {}
    data[request.from_user_id]['request'] = request
    question = session.query(Question).get(request.question_id)
    to_chat_kb = types.InlineKeyboardMarkup()
    to_chat_kb.inline_keyboard = [
        [types.InlineKeyboardButton(text="Go to chat🔥", callback_data="start_chat")]
    ]
    notification = await message.bot.send_message(chat_id=request.from_user_id,
                                                  text="Your request was accepted. Hurry up to the chat.",
                                                  reply_markup=to_chat_kb)
    await message.bot.pin_chat_message(chat_id=request.from_user_id, message_id=notification.message_id)
    await message.answer(text=f"You're in anonymous chat about question:\n"
                              f"\"{question.text}\"\n"
                              f"Please wait, your talker will connect soon...",
                         reply_markup=leave_chat_kb)
    await DialogueStates.chatting.set()


async def chatting(message: types.Message, state: FSMContext):
    """Chatting."""

    text = message.text
    user_data = await state.get_data()
    if 'request' in user_data:
        request = user_data['request']
    else:
        request = data[message.from_user.id]['request']
    if request.from_user_id == message.from_user.id:
        await message.bot.send_message(chat_id=request.to_user_id,
                                       text=text)
    else:
        await message.bot.send_message(chat_id=request.from_user_id,
                                       text=text)


async def leave_chat(message: types.Message, state: FSMContext):
    """Leave chat."""

    logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) left from anonymous chat.")
    user_data = await state.get_data()
    if 'request' in user_data:
        request = user_data['request']
    else:
        request = data[message.from_user.id]['request']
    if request.from_user_id == message.from_user.id:
        await message.bot.send_message(chat_id=request.to_user_id,
                                       text="Your talker left the chat :(")
    else:
        await message.bot.send_message(chat_id=request.from_user_id,
                                       text="Your talker left the chat :(")
    await CommonStates.to_main_menu.set()
    await send_user_to_main_menu(message, state)


def register_dialogue_handlers(dp: Dispatcher):
    """Registers all dialogue handlers on dispatcher."""

    dp.register_message_handler(start_chat, state=DialogueStates.start_chat)
    dp.register_message_handler(leave_chat, Text(equals="Leave chat"), state=DialogueStates.chatting)
    dp.register_message_handler(chatting, state=DialogueStates.chatting)

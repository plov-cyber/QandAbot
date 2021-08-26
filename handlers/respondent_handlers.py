"""Respondent handlers."""

# Libraries, classes and functions imports
import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from data import db_session
from data.UserModel import User
from handlers.states import RespondentStates, CommonStates

logger = logging.getLogger(__name__)

# Keyboards.
ok_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                                        keyboard=[[
                                            types.KeyboardButton(text="OK")
                                        ]])

# Creating session for db.
session = db_session.create_session()


async def reply_on_respondent(message: types.Message, state: FSMContext):
    """Different replies about respondent."""

    text = message.text
    user = session.query(User).get(message.from_user.id)
    if text == "Yeah, with pleasure 😜":
        user.is_respondent = 3
        session.merge(user)
        session.commit()
        logger.info(
            f"User {message.from_user.first_name}(@{message.from_user.username}) became a respondent.")
        await message.answer(text="You are respondent from this time, so be sure to check your mail sometimes.",
                             reply_markup=ok_keyboard)
        await RespondentStates.send_actions.set()
    elif text == "No, not right now":
        user.is_respondent = 2
        session.merge(user)
        session.commit()
        await message.answer(text="Next time, you will be able to become a responder without passing the test.",
                             reply_markup=ok_keyboard)
        await RespondentStates.send_actions.set()
    else:
        await message.answer(text="Oops, please choose one of two variants")


async def respondent_send_interactions(message: types.Message):
    """Interactions for respondent."""

    keyboard_for_interact = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True,
                                                      row_width=1)
    buttons = [
        types.KeyboardButton(text="My questions"),
        types.KeyboardButton(text="Available questions"),
        types.KeyboardButton(text="Requests")
    ]
    keyboard_for_interact.add(*buttons)
    await message.answer(text="Choose what you want to do:",
                         reply_markup=keyboard_for_interact)
    await RespondentStates.react_to_inters.set()


async def respondent_react_to_inters(message: types.Message, state: FSMContext):
    """Reacts to different interactions."""

    text = message.text
    if text == "Available questions":
        pass
    elif text == "Requests":
        pass


async def respondent_send_actions(message: types.Message):
    """Actions for respondent."""

    keyboard_for_respondent = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                                                        row_width=1)
    buttons = [
        types.KeyboardButton(text="Ask question"),
        types.KeyboardButton(text="Find question"),
        types.KeyboardButton(text="Interaction")
    ]
    keyboard_for_respondent.add(*buttons)
    await message.answer(text="The liability of the respondent includes:\n\n"
                              "1. Answer up to 10 questions about Innopolis\n"
                              "2. Respond with culture and respect to the question\n"
                              "3. Answer correctly\n"
                              "4. Please give full answers:\n"
                              "!!!Wrong: <s>It's so easy...</s>\n"
                              "a) If you want to find a question in data base:\n"
                              "-You need to send #Hashtags, which describe your question 🙋 \n"
                              "-After, you get some questions with the same #Hashtags\n"
                              "-Next, you can flip questions over by ⬅️➡️\n"
                              "b) If you want to create your question:\n"
                              "-You need to send the question\n"
                              "-After, send all #Hashtags in one message\n"
                              "-Next, you need only wait...",
                         parse_mode="HTML", reply_markup=keyboard_for_respondent)
    await CommonStates.react_to_actions.set()


def register_respondent_handlers(dp: Dispatcher):
    """Registers all respondent_handlers to dispatcher."""

    logger.info(msg=f"Registering respondent handlers.")
    dp.register_message_handler(reply_on_respondent, state=RespondentStates.wait_for_reply)
    dp.register_message_handler(respondent_send_actions, state=RespondentStates.send_actions)
    dp.register_message_handler(respondent_send_interactions, state=RespondentStates.send_interactions)
    dp.register_message_handler(respondent_react_to_inters, state=RespondentStates.react_to_inters)

"""Common User handlers."""

# Libraries, classes and functions imports
import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from data import db_session
from data.UserModel import User
from handlers.states import CommonUserStates, CommonStates, QuizStates, RespondentStates

logger = logging.getLogger(__name__)

# Keyboards.
keyboard_for_quiz = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buttons = [
    types.KeyboardButton(text="Give me this test!"),
    types.KeyboardButton(text="I prefer to do it later")
]
keyboard_for_quiz.add(*buttons)

ok_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                                        keyboard=[[
                                            types.KeyboardButton(text="OK")
                                        ]])

# Creating session for db.
session = db_session.create_session()


async def common_user_send_interactions(message: types.Message):
    """Interactions for common user."""

    await CommonUserStates.send_interactions.set()
    keyboard_for_interact = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True,
                                                      row_width=1)
    buttons = [
        types.KeyboardButton(text="My questions"),
        types.KeyboardButton(text="Become respondent"),
        types.KeyboardButton(text="Back to menu ↩️🥺")
    ]
    keyboard_for_interact.add(*buttons)
    await message.answer(text="Choose what you want to do:",
                         reply_markup=keyboard_for_interact)
    await CommonUserStates.react_to_inters.set()


async def common_user_react_to_inters(message: types.Message, state: FSMContext):
    """Reacts to different interactions."""

    text = message.text
    if text == 'Become respondent':
        user = session.query(User).get(message.from_user.id)
        if not user:
            logger.error(msg=f"Can't get user {message.from_user.first_name}(@{message.from_user.username})")
            await message.answer(text="Oops, something went wrong :(",
                                 reply_markup=types.ReplyKeyboardRemove())
            await state.finish()
        else:
            stat = user.is_respondent
            responses = ["To become a respondent you should pass the test.",
                         "To become a respondent you should take the test again."]
            if stat in [0, 1]:
                logger.info(
                    msg=f"User {message.from_user.first_name}(@{message.from_user.username}) wants to pass quiz.")
                await message.answer(text=responses[stat],
                                     reply_markup=keyboard_for_quiz)
                await QuizStates.wait_for_reply.set()
            elif stat == 2:
                user.is_respondent = 3
                session.merge(user)
                session.commit()
                logger.info(
                    f"User {message.from_user.first_name}(@{message.from_user.username}) became a respondent.")
                await message.answer(text="You already passed the test and can start answering the questions.",
                                     reply_markup=ok_keyboard)
                await RespondentStates.send_actions.set()


async def common_user_send_actions(message: types.Message):
    """Actions for common user."""

    keyboard_for_questions = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True,
                                                       row_width=1)
    buttons = [
        types.KeyboardButton(text="Ask question"),
        types.KeyboardButton(text="Find question"),
        types.KeyboardButton(text="Interaction")
    ]
    keyboard_for_questions.add(*buttons)
    await message.answer(text=f"-How to use Q&A Bot?\n"
                              f"-It's so easy in using:\n"
                              f"1. If you want to find a question in data base:\n"
                              f"    You need to send #Hashtags, which describe your question 🙋 \n"
                              f"    After, you get some questions with the same #Hashtags \n"
                              f"    Next, you can flip questions over by ⬅️➡️\n"
                              f"2. If you want to create your question:\n"
                              f"    You need to send the question\n"
                              f"    After, send all #Hashtags in one message\n"
                              f"    Next, you need only wait...", reply_markup=keyboard_for_questions)
    await CommonStates.react_to_actions.set()


def register_common_user_handlers(dp: Dispatcher):
    """Registers all common_user_handlers to dispatcher."""

    logger.info(msg=f"Registering common user handlers.")
    dp.register_message_handler(common_user_send_actions, state=CommonUserStates.send_actions)
    dp.register_message_handler(common_user_send_interactions, state=CommonUserStates.send_interactions)
    dp.register_message_handler(common_user_react_to_inters, state=CommonUserStates.react_to_inters)

"""Common User handlers."""

# Libraries, classes and functions imports
import logging

import requests
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from api import PORT
from handlers.common_handlers import keyboard_for_quiz
from handlers.quiz_handlers import ok_keyboard
from handlers.states import CommonUserStates, QuizStates, RespondentStates, FindQuestionStates, AskQuestionStates

logger = logging.getLogger(__name__)


async def common_user_send_actions(message: types.Message):
    """Actions for common user."""

    keyboard_for_questions = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True,
                                                       row_width=1)
    buttons = [
        types.KeyboardButton(text="Ask question"),
        types.KeyboardButton(text="Find question"),
        types.KeyboardButton(text="Become respondent")
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
    await CommonUserStates.next()


async def react_to_actions(message: types.Message, state: FSMContext):
    """Different reactions to actions."""

    text = message.text
    if text == "Become respondent":
        user = requests.get(f"http://localhost:{PORT}/api_users/{message.from_user.id}").json()
        if "message" in user:
            logger.error(msg=f"Can't get user {message.from_user.first_name}(@{message.from_user.username})")
            await message.answer(text="Oops, something went wrong :(",
                                 reply_markup=types.ReplyKeyboardRemove())
            await state.finish()
        else:
            user = user['user']
            stat = user['is_respondent']
            responses = ["To become a respondent you should pass the test.",
                         "To become a respondent you should take the test again."]
            if stat in [0, 1]:
                await message.answer(text=responses[stat],
                                     reply_markup=keyboard_for_quiz)
                await QuizStates.wait_for_reply.set()
            elif stat == 2:
                res = requests.put(f"http://localhost:{PORT}/api_users/{message.from_user.id}", json={
                    'is_respondent': 3
                }).json()
                if 'success' in res:
                    await message.answer(text="You already passed the test and can start answering the questions.",
                                         reply_markup=ok_keyboard)
                    await RespondentStates.send_actions.set()
                else:
                    logger.error(msg=f"Can't set is_respondent to 3 "
                                     f"for {message.from_user.first_name}(@{message.from_user.username}).")
                    await message.answer(text="Oops, something went wrong :(",
                                         reply_markup=types.ReplyKeyboardRemove())
                    await state.finish()
    elif text == "Ask question":
        await message.answer(text="Goood choice👍 Please send me your question⁉️:",
                             reply_markup=types.ReplyKeyboardRemove())
        await AskQuestionStates.getting_question.set()
    elif text == "Find question":
        await message.answer("So goood 👍 Send me hashtags, which describe your question:",
                             reply_markup=types.ReplyKeyboardRemove())
        await FindQuestionStates.getting_hashtags.set()


def register_common_user_handlers(dp: Dispatcher):
    """Registers all common_user_handlers to dispatcher."""

    logger.info(msg=f"Registering common user handlers.")
    dp.register_message_handler(common_user_send_actions, state=CommonUserStates.send_actions)
    dp.register_message_handler(react_to_actions, state=CommonUserStates.react_to_actions)

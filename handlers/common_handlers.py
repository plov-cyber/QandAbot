"""Common handlers."""

# Libraries, classes and functions imports
import logging

import requests
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from api import PORT
from handlers.common_user_handlers import common_user_send_actions, common_user_send_interactions
from handlers.respondent_handlers import respondent_send_actions, respondent_send_interactions
from handlers.states import QuizStates, RespondentStates, CommonUserStates, AskQuestionStates, FindQuestionStates, \
    CommonStates

logger = logging.getLogger(__name__)

# Keyboard asking about passing quiz.
keyboard_for_quiz = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buttons = [
    types.KeyboardButton(text="Give me this test!"),
    types.KeyboardButton(text="I prefer to do it later")
]
keyboard_for_quiz.add(*buttons)


async def cmd_start(message: types.Message, state: FSMContext):
    """Function triggers on /start."""

    logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) sent /start command.")
    await state.finish()
    user = requests.get(f'http://localhost:{PORT}/api_users/{message.from_user.id}').json()
    if 'user' in user:
        await send_user_to_main_menu(message)
    else:
        requests.post(f'http://localhost:{PORT}/api_users', json={
            'id': message.from_user.id,
            'username': message.from_user.username,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name if message.from_user.last_name else ""
        }).json()
        logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) successfully registered.")
        user_name = message.from_user.first_name + ' ' + message.from_user.last_name \
            if message.from_user.last_name else message.from_user.first_name
        await message.answer(text=f"Hi 👋🏼 {user_name}.\n"
                                  f"You successfully registered and you have access to the questions database🎉🎉🎉\n"
                                  f"However, in order to answer on the questions and earn Innopoints you have to pass"
                                  f" a fascinating test to determine your competence in different spheres.",
                             reply_markup=keyboard_for_quiz)
        await QuizStates.wait_for_reply.set()


async def cmd_help(message: types.Message, state: FSMContext):
    """Function triggers on /help."""

    logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) sent /help command.")
    await state.finish()
    await message.answer(text="It’s an up-to-date Bot with a database of questions that were answered with competent "
                              "answers. You always can contact developer:\n"
                              "📩: l.rekhlov@innopolis.university\n"
                              "📩: s.kamalov@innopolis.university\n"
                              "telegram: @RRMOLL\n", reply_markup=types.ReplyKeyboardRemove())


async def cmd_cancel(message: types.Message):
    """Function triggers on /cancel."""

    logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) sent /cancel command.")
    await send_user_to_main_menu(message)


async def send_user_to_main_menu(message: types.Message):
    """Sends user to main menu."""

    logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) is in main menu now.")
    user = requests.get(f"http://localhost:{PORT}/api_users/{message.from_user.id}").json()
    if "message" in user:
        logger.error(msg=f"Can't get user {message.from_user.first_name}(@{message.from_user.username})")
        await message.answer(text="Oops, something went wrong :(",
                             reply_markup=types.ReplyKeyboardRemove())
    else:
        user = user['user']
        stat = user['is_respondent']
        if stat in [0, 1, 2]:
            await CommonUserStates.send_actions.set()
            await common_user_send_actions(message)
        elif stat == 3:
            await RespondentStates.send_actions.set()
            await respondent_send_actions(message)


async def react_to_actions(message: types.Message, state: FSMContext):
    """Different reactions to actions."""

    text = message.text
    if text == "Interaction":
        logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) opened Interaction menu.")
        user = requests.get(f'http://localhost:{PORT}/api_users/{message.from_user.id}').json()
        if 'message' in user:
            logger.error(msg=f"Can't find user {message.from_user.first_name}(@{message.from_user.username}).")
            await message.answer(text="Oops, something went wrong :(",
                                 reply_markup=types.ReplyKeyboardRemove())
            await state.finish()
            return

        user = user['user']
        stat = user['is_respondent']
        if stat in [0, 1, 2]:
            await CommonUserStates.send_interactions.set()
            await common_user_send_interactions(message)
        elif stat == 3:
            await RespondentStates.send_interactions.set()
            await respondent_send_interactions(message)

    if text == "Ask question":
        logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) asking a question.")
        await message.answer(text="Goood choice👍 Please send me your question⁉️:",
                             reply_markup=types.ReplyKeyboardRemove())
        await AskQuestionStates.getting_question.set()
    elif text == "Find question":
        logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) finding a question.")
        await message.answer("So goood 👍 Send me hashtags, which describe your question:",
                             reply_markup=types.ReplyKeyboardRemove())
        await FindQuestionStates.getting_hashtags.set()


def register_common_handlers(dp: Dispatcher):
    """Registers all common_handlers to dispatcher."""

    logger.info(msg=f"Registering common handlers.")
    dp.register_message_handler(cmd_start, commands='start', state="*")
    dp.register_message_handler(cmd_help, commands='help', state='*')
    dp.register_message_handler(cmd_cancel, commands='cancel', state="*")
    dp.register_message_handler(react_to_actions, state=CommonStates.react_to_actions)

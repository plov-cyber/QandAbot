"""Common handlers."""

# Libraries, classes and functions imports
import requests
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from api import PORT
from data import db_session
from data.UserModel import User
from handlers.states import QuizStates

# Keyboard asking about passing quiz.
keyboard_for_quiz = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buttons = [
    types.KeyboardButton(text="Give me this test!"),
    types.KeyboardButton(text="Skip the test")
]
keyboard_for_quiz.add(*buttons)


async def cmd_start(message: types.Message, state: FSMContext):
    """Function triggers on /start."""

    await state.finish()
    user = requests.get(f'http://localhost:{PORT}/api_users/{message.from_user.id}').json()
    if 'message' not in user:
        user = user['user']
        await message.answer(text="There is nothing here yet. :(")
        if user['is_respondent'] == 2:
            pass
    else:
        requests.post(f'http://localhost:{PORT}/api_users', json={
            'id': message.from_user.id,
            'username': message.from_user.username,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name if message.from_user.last_name else ""
        }).json()
        user_name = message.from_user.first_name + ' ' + message.from_user.last_name \
            if message.from_user.last_name else message.from_user.first_name
        await message.answer(text=f"Hi 👋🏼 {user_name}.\n"
                                  f"You successfully registered and you have access to the questions database🎉🎉🎉.\n"
                                  f"However, in order to leave your question you have to pass a fascinating test"
                                  f" to determine your competence in different spheres.",
                             reply_markup=keyboard_for_quiz)
        await QuizStates.wait_for_reply.set()


async def cmd_help(message: types.Message, state: FSMContext):
    """Function triggers on /help."""

    await state.finish()
    await message.answer(text="It’s an up-to-date Bot with a database of questions that were answered with competent "
                              "answers. You always can contact developer:\n"
                              "📩: l.rekhlov@innopolis.university\n"
                              "📩: s.kamalov@innopolis.university\n"
                              "telegram: @RRMOLL\n", reply_markup=types.ReplyKeyboardRemove())


def register_common_handlers(dp: Dispatcher):
    """Registers all common_handlers to dispatcher."""

    dp.register_message_handler(cmd_start, commands='start', state="*")
    dp.register_message_handler(cmd_help, commands='help', state='*')

"""Handlers for asking questions."""

# Libraries, classes and functions imports
import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from api import PORT, req
from handlers.common_handlers import send_user_to_main_menu
from handlers.states import AskQuestionStates, CommonStates

logger = logging.getLogger(__name__)


async def get_question(message: types.Message, state: FSMContext):
    """Gets question from user."""

    question = message.text
    res = req.post(f'http://localhost:{PORT}/api_questions', json={
        'text': question,
        'is_answered': False,
        'from_user_id': message.from_user.id
    }).json()
    if 'success' not in res:
        await message.answer(text="This question already exists")
        return

    await state.update_data(question=question)
    logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) asked a question.")
    await message.answer(text=f"Fine 😸 Now write all #hashtags in one message to this question like this (#dorm):")
    await AskQuestionStates.getting_hashtags.set()


async def get_hashtags(message: types.Message, state: FSMContext):
    """Gets hashtags for question from user."""

    user_data = await state.get_data()

    hashtags = message.text
    if hashtags[0] != '#':
        await message.answer(text="Please write hashtags like this: #hashtag1#hashtag2...")
        return

    hashtags = hashtags[1:].lower().split('#')
    for h in hashtags:
        h = h.strip()
        res = req.post(f'http://localhost:{PORT}/api_hashtags', json={
            'text': h,
            'question': user_data['question']
        }).json()

    logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username})"
                    f" wrote hashtags for question \"{user_data['question']}\".")
    await message.answer(text="Ohh thanks for question, It joins to the work ⚙️ We will notify you 📩")
    await CommonStates.to_main_menu.set()
    await send_user_to_main_menu(message, state)


def register_ask_question_handlers(dp: Dispatcher):
    """Registers all ask_question_handlers to dispatcher."""

    logger.info(msg="Registering ask_question handlers.")
    dp.register_message_handler(get_question, state=AskQuestionStates.getting_question)
    dp.register_message_handler(get_hashtags, state=AskQuestionStates.getting_hashtags)

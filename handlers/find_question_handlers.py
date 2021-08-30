"""Handlers for finding questions."""

# Libraries, classes and functions imports
import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from handlers.common_handlers import send_user_to_main_menu
from handlers.states import FindQuestionStates, CommonStates
from helpers import find_questions_by_hashtags

logger = logging.getLogger(__name__)

is_answered_signs = ['❌', '✅']


async def get_hashtags(message: types.Message, state: FSMContext):
    """Gets hashtags from user and finds questions."""

    hashtags = message.text
    if hashtags[0] != '#':
        await message.answer(text="Please write hashtags like this: #hashtag1#hashtag2...")
        return

    hashtags = [h.strip() for h in hashtags[1:].lower().split('#')]
    logger.info(msg=f"Got hashtags from user {message.from_user.first_name}(@{message.from_user.username}).")

    suit_questions = find_questions_by_hashtags(hashtags)
    size = len(suit_questions)
    await state.reset_data()
    if size:
        logger.info(
            msg=f"Showing questions to "
                f"user {message.from_user.first_name}(@{message.from_user.username}) for hashtags {hashtags}.")
        buttons = [
            [types.InlineKeyboardButton(text='⬅️', callback_data="previous_question"),
             types.InlineKeyboardButton(text=f'1/{size}', callback_data="question_num"),
             types.InlineKeyboardButton(text='➡️', callback_data="next_question")]
        ]
        if suit_questions[0].is_answered:
            buttons.append([types.InlineKeyboardButton(text="Show answer", callback_data="show_answer")])
        buttons.append([types.InlineKeyboardButton(text="Back to menu ↩️🥺", callback_data="go_back")])
        showing_questions_keyboard = types.InlineKeyboardMarkup(row_width=3)
        showing_questions_keyboard.inline_keyboard = buttons
        await state.update_data(index=0, questions=suit_questions, message=message, show_answer=False,
                                request_sent=False)
        await message.answer(text=f"Question:\n"
                                  f"{suit_questions[0].text}\n\n"
                                  f"Answered: {is_answered_signs[suit_questions[0].is_answered]}",
                             reply_markup=showing_questions_keyboard)
        await FindQuestionStates.show_questions.set()
    else:
        await message.answer(text="Sorry, but there are no questions.")
        await CommonStates.to_main_menu.set()
        await send_user_to_main_menu(message, state)


def register_find_question_handlers(dp: Dispatcher):
    """Registers all find_question_handler to dispatcher."""

    logger.info(msg=f"Registering find_question handlers.")
    dp.register_message_handler(get_hashtags, state=FindQuestionStates.getting_hashtags)

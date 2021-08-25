"""Respondent handlers."""

# Libraries, classes and functions imports
import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from api import PORT, req
from handlers.quiz_handlers import ok_keyboard
from handlers.states import RespondentStates, CommonStates

logger = logging.getLogger(__name__)


async def reply_on_respondent(message: types.Message, state: FSMContext):
    """Different replies about respondent."""

    text = message.text
    if text == "Yeah, with pleasure 😜":
        res = req.put(f"http://localhost:{PORT}/api_users/{message.from_user.id}", json={
            'is_respondent': 3
        }).json()
        if 'success' in res:
            logger.info(
                f"User {message.from_user.first_name}(@{message.from_user.username}) became a respondent.")
            await message.answer(text="You are respondent from this time, so be sure to check your mail sometimes.",
                                 reply_markup=ok_keyboard)
            await RespondentStates.send_actions.set()
        else:
            logger.error(msg=f"Can't set is_respondent to 3 "
                             f"for {message.from_user.first_name}(@{message.from_user.username}).")
            await message.answer(text="Oops, something went wrong :(",
                                 reply_markup=types.ReplyKeyboardRemove())
            await state.finish()
    elif text == "No, not right now":
        res = req.put(f"http://localhost:{PORT}/api_users/{message.from_user.id}", json={
            'is_respondent': 2
        }).json()
        if 'success' in res:
            await message.answer(text="Next time, you will be able to become a responder without passing the test.",
                                 reply_markup=ok_keyboard)
            await RespondentStates.send_actions.set()
        else:
            logger.error(msg=f"Can't set is_respondent to 2 "
                             f"for {message.from_user.first_name}(@{message.from_user.username}).")
            await message.answer(text="Oops, something went wrong :(",
                                 reply_markup=types.ReplyKeyboardRemove())
            await state.finish()
    else:
        await message.answer(text="Oops, please choose one of two variants")


async def respondent_send_interactions(message: types.Message):
    """Interactions for respondent."""

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

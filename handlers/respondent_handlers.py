"""Respondent handlers."""
import requests
from aiogram import types, Dispatcher

from api import PORT
from handlers.states import RespondentStates


async def reply_on_respondent(message: types.Message):
    """Different replies about respondent."""

    text = message.text
    if text == "Yes, with pleasure":
        res = requests.put(f"http://localhost:{PORT}/api_users/{message.from_user.id}", json={
            'is_respondent': 2
        }).json()
        if 'success' in res:
            await message.answer(text="Congratulations! Now you can answer questions.",
                                 reply_markup=types.ReplyKeyboardRemove())
        else:
            await message.answer(text="Fuck, it doesn't work!",
                                 reply_markup=types.ReplyKeyboardRemove())
    elif text == "No, not now":
        pass
    else:
        await message.answer(text="Oops, please choose one of two variants")


def register_respondent_handlers(dp: Dispatcher):
    """Registers all respondent_handlers to dispatcher."""

    dp.register_message_handler(reply_on_respondent, state=RespondentStates.wait_for_reply)

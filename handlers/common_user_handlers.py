"""Common User handlers."""

# Libraries, classes and functions imports
from aiogram import types, Dispatcher

from handlers.states import CommonUserStates


async def common_user_send_actions(message: types.Message):
    """Actions for common user."""

    keyboard_for_questions = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True,
                                                       row_width=1)
    buttons = [
        types.KeyboardButton(text="Ask question"),
        types.KeyboardButton(text="Find solution"),
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


def register_common_user_handlers(dp: Dispatcher):
    """Registers all common_user_handlers to dispatcher."""

    dp.register_message_handler(common_user_send_actions, state=CommonUserStates.send_actions)

"""Quiz handlers."""

# Libraries, classes and functions imports
import asyncio
import logging
from time import time
from random import shuffle

import requests
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from api import PORT
from handlers.quiz_text import QUIZ
from handlers.states import RespondentStates, QuizStates, CommonUserStates

logger = logging.getLogger(__name__)

# Dictionary with all users.
quiz_dict = {}

ok_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                                        keyboard=[[
                                            types.KeyboardButton(text="OK")
                                        ]])


async def reply_on_quiz(message: types.Message, state: FSMContext):
    """Different replies before quiz."""

    text = message.text
    if text == "Skip the test":
        await state.finish()
        await message.answer(text="You can always return to the test to be able to answer questions.",
                             reply_markup=ok_keyboard)
        await CommonUserStates.send_actions.set()
    elif text == "Give me this test!":
        await state.finish()
        quests = list(QUIZ.keys())
        shuffle(quests)
        quiz_dict[message.from_user.id] = {
            "num": -1,
            "quests": quests,
            "result": 0
        }
        await passing_quiz(message)
    else:
        await message.answer(text="Oops, please choose one of two variants")


async def passing_quiz(message: types.Message):
    """Function sending the quiz."""

    data = quiz_dict[message.from_user.id]
    if data["num"] == -1:
        logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) starts passing the quiz.")
        await message.answer(text="Test will start in", reply_markup=types.ReplyKeyboardRemove())
        for i in range(3, 0, -1):
            await message.answer(text=f"{i}")
            await asyncio.sleep(1)
        data["num"] += 1
        await passing_quiz(message)
        return

    p_quests = data["quests"]
    i = data["num"]
    options = QUIZ[p_quests[i]]
    shuffle(options[1])
    now_question = await message.answer_poll(question=p_quests[i], options=options[1], is_anonymous=False,
                                             type="quiz", open_period=10,
                                             allows_multiple_answers=False,
                                             correct_option_id=options[1].index(options[0]))
    quiz_dict[message.from_user.id]["poll"] = now_question
    data["num"] += 1
    start_time = time()

    while not now_question.poll.is_closed and time() - start_time < 10:
        await asyncio.sleep(0.1)

    if data["num"] == 20:
        logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) passed the quiz.")
        data["result"] = int(100 * (data["result"] / 20))
        await message.answer(text=f"My congratulations, you know Innopolis on {data['result']}%")

        if data["result"] >= 40:
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            buttons = [
                types.KeyboardButton(text="Yes, with pleasure"),
                types.KeyboardButton(text="No, not now")
            ]
            keyboard.add(*buttons)
            await message.answer(text="Would you like to be respondent?", reply_markup=keyboard)
            await RespondentStates.wait_for_reply.set()
        else:
            res = requests.put(f"http://localhost:{PORT}/api_users/{message.from_user.id}", json={
                'is_respondent': 1
            }).json()
            if 'success' in res:
                await message.answer(text="Unfortunately, you failed the test,\n"
                                          "but it will be available again soon.", reply_markup=ok_keyboard)
                # тест должен появляться снова через неделю
                await CommonUserStates.send_actions.set()
            else:
                await message.answer(text=f"Can't set is_respondent to 1 for @{message.from_user.username} :(")

        quiz_dict.pop(message.from_user.id)
        return

    await passing_quiz(message)


async def getting_quiz_answer(poll_answer: types.PollAnswer):
    """Counting user's right answers."""

    quiz_dict[poll_answer.user.id]["poll"].poll.is_closed = True

    right_answer = quiz_dict[poll_answer.user.id]["poll"].poll.correct_option_id
    user_answer = poll_answer.option_ids[0]
    if right_answer == user_answer:
        quiz_dict[poll_answer.user.id]["result"] += 1


def register_quiz_handlers(dp: Dispatcher):
    """Registers all quiz_handlers to dispatcher."""

    logger.info(msg=f"Registering quiz handlers.")
    dp.register_message_handler(reply_on_quiz, state=QuizStates.wait_for_reply)
    dp.register_poll_answer_handler(getting_quiz_answer)

import asyncio
from random import shuffle

from aiogram import Dispatcher, types

from handlers.quiz_text import QUIZ
from handlers.states import QuizStates


async def reply_on_quiz(message: types.Message):
    text = message.text
    if text == "Skip the test":
        pass
    elif text == "Give me this test!":
        await QuizStates.next()
        quests = list(QUIZ.keys)
        shuffle(quests)
        data = {
            "num": -1,
            "quests": quests
        }
        await passing_quiz(message, data)
    else:
        await message.answer(text="Oops, please choose one of two variants")


async def passing_quiz(message: types.Message, data: dict):
    if data == -1:
        await message.answer(text="Test will start in", reply_markup=types.ReplyKeyboardRemove())
        for i in range(3, 0, -1):
            await asyncio.sleep(2)
            await message.answer(text=f"{i}")
        data["num"] += 1
        await passing_quiz(message, data)
    else:
        p_quests = data["quests"]
        i = data["num"]
        options = QUIZ[p_quests[i]]
        now_question = message.answer_poll(question=p_quests[i], options=options[1], is_anonymous=False, type="quiz",
                                           allows_multiple_answers=False, correct_option_id=options[0])


def register_quiz_handlers(dp: Dispatcher):
    dp.register_message_handler(reply_on_quiz, state=QuizStates.wait_for_reply)

import asyncio
from random import shuffle

from aiogram import Dispatcher, types

from handlers.quiz_text import QUIZ
from handlers.states import QuizStates

quiz_dict = {}


async def reply_on_quiz(message: types.Message):
    text = message.text
    if text == "Skip the test":
        pass
    elif text == "Give me this test!":
        await QuizStates.next()
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
    data = quiz_dict[message.from_user.id]
    if data["num"] == -1:
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
                                             type="quiz", open_period=15,
                                             allows_multiple_answers=False,
                                             correct_option_id=options[1].index(options[0]))
    quiz_dict[message.from_user.id]["poll"] = now_question
    data["num"] += 1

    while not now_question.poll.is_closed:
        await asyncio.sleep(0.1)

    if data["num"] == 17:  # исправить потом
        await message.answer(text=f"Nice job! Your result is {data['result']}/17.")
        return

    await passing_quiz(message)


async def getting_quiz_answer(poll_answer: types.PollAnswer):
    quiz_dict[poll_answer.user.id]["poll"].poll.is_closed = True

    right_answer = quiz_dict[poll_answer.user.id]["poll"].poll.correct_option_id
    user_answer = poll_answer.option_ids[0]
    if right_answer == user_answer:
        quiz_dict[poll_answer.user.id]["result"] += 1


def register_quiz_handlers(dp: Dispatcher):
    dp.register_message_handler(reply_on_quiz, state=QuizStates.wait_for_reply)
    # dp.register_message_handler(passing_quiz, state=QuizStates.quiz)
    dp.register_poll_answer_handler(getting_quiz_answer)

"""Quiz handlers."""

# Libraries, classes and functions imports
import asyncio
from random import shuffle

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from handlers.quiz_text import QUIZ
from handlers.states import RespondentStates, QuizStates

# Dictionary with all users.
quiz_dict = {}


async def reply_on_quiz(message: types.Message, state: FSMContext):
    """Different replies before quiz."""

    text = message.text
    if text == "Skip the test":
        await state.finish()
        await message.answer(text=f"-How to use Q&A Bot?\n"
                                  f"-It's so easy in using:\n"
                                  f"1. If you want to find a question in data base:\n"
                                  f"    You need to send #Hashtags, which describe your question 🙋 \n"
                                  f"    After, you get some questions with the same #Hashtags \n"
                                  f"    Next, you can flip questions over by ⬅️➡️\n"
                                  f"2. If you want to create your question:\n"
                                  f"    You need to send the question\n"
                                  f"    After, send all #Hashtags in one message\n"
                                  f"    Next, you need only wait...", reply_markup=types.ReplyKeyboardRemove())
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

    while not now_question.poll.is_closed:
        await asyncio.sleep(0.1)

    if data["num"] == 17:  # исправить
        data["result"] = int(100 * (data["result"] / 17))
        await message.answer(text=f"My congratulations, you know Innopolis on {data['result']}%")

        if data["result"] >= 40:
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            buttons = [
                types.KeyboardButton(text="Yes, with pleasure"),
                types.KeyboardButton(text="No, not now")
            ]
            keyboard.add(*buttons)
            await message.answer(text="Would you like to be respondent?")
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
                                 parse_mode="HTML", reply_markup=keyboard)
            await RespondentStates.wait_for_reply.set()
        else:
            pass  # доделать

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

    dp.register_message_handler(reply_on_quiz, state=QuizStates.wait_for_reply)
    dp.register_poll_answer_handler(getting_quiz_answer)

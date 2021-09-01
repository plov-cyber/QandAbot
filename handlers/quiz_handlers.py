"""Quiz handlers."""

# Libraries, classes and functions imports
import asyncio
import logging
from random import shuffle
from time import time

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from data import db_session
from data.UserModel import User
from handlers.common_handlers import send_user_to_main_menu
from handlers.quiz_text import QUIZ
from handlers.states import RespondentStates, QuizStates, CommonUserStates, CommonStates

logger = logging.getLogger(__name__)

# Dictionary with all users.
quiz_dict = {}

ok_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                                        keyboard=[[
                                            types.KeyboardButton(text="OK")
                                        ]])

# Creating session for db.
session = db_session.create_session()


async def reply_on_quiz(message: types.Message, state: FSMContext):
    """Different replies before quiz."""

    text = message.text
    if text == "I prefer to do it later...":
        logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) skipped the test.")
        await CommonStates.to_main_menu.set()
        await send_user_to_main_menu(message, state)
    elif text == "Give me this test!":
        logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) starts passing the quiz.")
        quests = list(QUIZ.keys())
        shuffle(quests)
        quests = quests[:20]
        quiz_dict[message.from_user.id] = {
            "num": -1,
            "quests": quests,
            "result": 0
        }
        await QuizStates.passing_quiz.set()
        await passing_quiz(message, state)
    else:
        await message.answer(text="Oops, please choose one of two variants")


async def passing_quiz(message: types.Message, state: FSMContext):
    """Function sending the quiz."""

    data = quiz_dict[message.from_user.id]
    if data["num"] == -1:
        await message.answer(text="Test will start in", reply_markup=types.ReplyKeyboardRemove())
        for i in range(3, 0, -1):
            await message.answer(text=f"{i}")
            await asyncio.sleep(0.5)
        data["num"] += 1
        await passing_quiz(message, state)
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
        await asyncio.sleep(0.01)

    if data["num"] == 20:
        logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) passed the quiz.")
        user = session.query(User).get(message.from_user.id)
        data["result"] = int(100 * (data["result"] / 20))
        user.rating = round(data['result'] / 20, 1)
        await message.answer(text=f"My congratulations, you know Innopolis on {data['result']}%")

        if data["result"] >= 40:
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            buttons = [
                types.KeyboardButton(text="Yeah, with pleasure 😜"),
                types.KeyboardButton(text="No, not right now")
            ]
            keyboard.add(*buttons)
            await message.answer(text="Would you like to be respondent\n"
                                      "and the most active resident of the Innopolis?", reply_markup=keyboard)
            await RespondentStates.wait_for_reply.set()
        else:
            user.is_respondent = 1
            logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) failed the test.")
            await message.answer(text="Unfortunately 😿 You failed test,\n"
                                      "that is why we recommend you to walk\n"
                                      "around of the city, learn something new\n"
                                      "and retake this test in a week💪🏼🤙🏼", reply_markup=ok_keyboard)
            # тест должен появляться снова через неделю
            await CommonUserStates.send_actions.set()

        session.merge(user)
        session.commit()
        quiz_dict.pop(message.from_user.id)
        return

    if await state.get_state() == 'QuizStates:passing_quiz':
        await passing_quiz(message, state)


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
    dp.register_message_handler(passing_quiz, state=QuizStates.passing_quiz)

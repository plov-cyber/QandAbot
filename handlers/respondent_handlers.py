"""Respondent handlers."""

# Libraries, classes and functions imports
import asyncio
import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from data import db_session
from data.AnswerModel import Answer
from data.QuestionModel import Question
from data.UserModel import User
from handlers.states import RespondentStates, CommonStates
from helpers import find_questions_by_hashtags

logger = logging.getLogger(__name__)

# Keyboards.
ok_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                                        keyboard=[[
                                            types.KeyboardButton(text="OK")
                                        ]])

# Creating session for db.
session = db_session.create_session()


async def reply_on_respondent(message: types.Message, state: FSMContext):
    """Different replies about respondent."""

    text = message.text
    user = session.query(User).get(message.from_user.id)
    if text == "Yeah, with pleasure 😜":
        user.is_respondent = 3
        session.merge(user)
        session.commit()
        logger.info(
            f"User {message.from_user.first_name}(@{message.from_user.username}) became a respondent.")
        await message.answer(text="You are respondent from this time, so be sure to check your mail sometimes.",
                             reply_markup=ok_keyboard)
        await RespondentStates.send_actions.set()
    elif text == "No, not right now":
        user.is_respondent = 2
        session.merge(user)
        session.commit()
        await message.answer(text="Next time, you will be able to become a responder without passing the test.",
                             reply_markup=ok_keyboard)
        await RespondentStates.send_actions.set()
    else:
        await message.answer(text="Oops, please choose one of two variants")


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


async def respondent_send_interactions(message: types.Message):
    """Interactions for respondent."""

    keyboard_for_interact = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True,
                                                      row_width=1)
    buttons = [
        types.KeyboardButton(text="My questions"),
        types.KeyboardButton(text="My answers"),
        types.KeyboardButton(text="Available questions"),
        types.KeyboardButton(text="Requests"),
        types.KeyboardButton(text="Back to menu ↩️🥺")
    ]
    keyboard_for_interact.add(*buttons)
    await message.answer(text="Choose what you want to do:",
                         reply_markup=keyboard_for_interact)
    await RespondentStates.react_to_inters.set()


async def respondent_react_to_inters(message: types.Message):
    """Reacts to different interactions."""

    text = message.text
    if text == "Available questions":
        keyboard = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
        buttons = [
            types.KeyboardButton(text="Find by #"),
            types.KeyboardButton(text="Scroll all questions")
        ]
        keyboard.add(*buttons)
        await message.answer(text="Do you want to find question by # or scroll all questions?",
                             reply_markup=keyboard)
        await RespondentStates.ask_for_available_questions.set()
    elif text == "Requests":
        pass


async def respondent_ask_for_available_questions(message: types.Message, state: FSMContext):
    """Asks respondent about how to find available questions."""

    text = message.text
    if text == "Find by #":
        await message.answer(text="Nice)) The most popular topics nowadays are:\n"
                                  "#dorm\n"
                                  "#university\n"
                                  "#lecture\n"
                                  "#professor", reply_markup=types.ReplyKeyboardRemove())
        await message.answer(text="💁🏽‍♂️Sand me plz the # in which category you want to get questions")
        await RespondentStates.show_available_questions.set()
    elif text == "Scroll all questions":
        await RespondentStates.show_available_questions.set()
        await respondent_show_available_questions(message, state)


async def respondent_show_available_questions(message: types.Message, state: FSMContext):
    """Shows available questions to respondent."""

    await state.reset_data()

    text = message.text
    if text == "Scroll all questions":
        questions = session.query(Question).filter(Question.is_answered == 0 and
                                                   Question.from_user_id != message.from_user.id).all()
    elif text[0] == "#":
        hashtags = [h.strip() for h in text[1:].lower().split("#")]
        questions = list(filter(lambda x: not x.is_answered and x.from_user_id != message.from_user.id,
                                find_questions_by_hashtags(hashtags)))
    else:
        await message.answer(text="Please write hashtags like this: #hashtag1#hashtag2...")
        return
    size = len(questions)
    if size:
        logger.info(msg=f"Showing available questions to respondent "
                        f"{message.from_user.first_name}(@{message.from_user.username}).")
        buttons = [
            [types.InlineKeyboardButton(text='⬅️', callback_data="previous_question"),
             types.InlineKeyboardButton(text=f'1/{size}', callback_data="question_num"),
             types.InlineKeyboardButton(text='➡️', callback_data="next_question")],
            [types.InlineKeyboardButton(text='Give answer', callback_data='give_answer')],
            [types.InlineKeyboardButton(text="Back to menu ↩️🥺", callback_data='go_back')]
        ]
        available_questions_keyboard = types.InlineKeyboardMarkup(row_width=3)
        available_questions_keyboard.inline_keyboard = buttons
        await state.update_data(index=0, questions=questions, message=message)
        await message.answer(text=f"Question:\n"
                                  f"{questions[0].text}",
                             reply_markup=available_questions_keyboard)
    else:
        await message.answer(text="Sorry, but there are no questions.")
        await asyncio.sleep(0.5)
        await RespondentStates.send_interactions.set()
        await respondent_send_interactions(message)


async def respondent_give_answer(message: types.Message, state: FSMContext):
    """Creates answer on question."""

    user_data = await state.get_data()
    question = user_data['question']
    logger.info(msg=f"Respondent {message.from_user.first_name}"
                    f"(@{message.from_user.username}) is giving answer on question \"{question.text}\".")
    answer_text = message.text
    answer = Answer(
        text=answer_text,
        from_user_id=message.from_user.id,
        question_id=question.id
    )
    question.is_answered = True
    session.merge(question)
    session.add(answer)
    session.commit()
    user = session.query(User).get(question.from_user_id)
    notification = await message.bot.send_message(chat_id=user.chat_id,
                                                  text=f"✉️ Your question\n\"{question.text}\"\n"
                                                       f"has been answered ✉️")
    await message.bot.pin_chat_message(chat_id=user.chat_id, message_id=notification.message_id)
    await message.answer(text="We appreciate you for answer.")
    logger.info(msg=f"Respondent {message.from_user.first_name}(@{message.from_user.username}) "
                    f"gave answer on question \"{question.text}\".")
    await RespondentStates.send_interactions.set()
    await respondent_send_interactions(message)


async def respondent_show_answers(message: types.Message, state: FSMContext):
    """Shows respondent's answers."""

    await RespondentStates.show_answers.set()
    answers = session.query(Answer).filter(Answer.from_user_id == message.from_user.id).all()
    size = len(answers)
    if size:
        logger.info(msg=f"Showing respondent's "
                        f"{message.from_user.first_name}(@{message.from_user.username}) answers.")
        buttons = [
            [types.InlineKeyboardButton(text='⬅️', callback_data="previous_question"),
             types.InlineKeyboardButton(text=f'1/{size}', callback_data="question_num"),
             types.InlineKeyboardButton(text='➡️', callback_data="next_question")],
            [types.InlineKeyboardButton(text="Back to menu ↩️🥺", callback_data='go_back')]
        ]
        show_answers_keyboard = types.InlineKeyboardMarkup(row_width=3)
        show_answers_keyboard.inline_keyboard = buttons
        await state.update_data(index=0, answers=answers, message=message)
        await message.answer(text=f"Question:\n"
                                  f"{answers[0].question.text}\n\n"
                                  f"Your answer:\n"
                                  f"{answers[0].text}",
                             reply_markup=show_answers_keyboard)
    else:
        await message.answer(text="Sorry, but you didn't give any answers.")
        await asyncio.sleep(0.5)
        await RespondentStates.send_interactions.set()
        await respondent_send_interactions(message)


def register_respondent_handlers(dp: Dispatcher):
    """Registers all respondent_handlers to dispatcher."""

    logger.info(msg=f"Registering respondent handlers.")
    dp.register_message_handler(reply_on_respondent, state=RespondentStates.wait_for_reply)
    dp.register_message_handler(respondent_send_actions, state=RespondentStates.send_actions)
    dp.register_message_handler(respondent_send_interactions, state=RespondentStates.send_interactions)
    dp.register_message_handler(respondent_show_answers, Text(equals="My answers"),
                                state=RespondentStates.react_to_inters)
    dp.register_message_handler(respondent_react_to_inters, state=RespondentStates.react_to_inters)
    dp.register_message_handler(respondent_ask_for_available_questions,
                                state=RespondentStates.ask_for_available_questions)
    dp.register_message_handler(respondent_show_available_questions, state=RespondentStates.show_available_questions)
    dp.register_message_handler(respondent_give_answer, state=RespondentStates.give_answer)
    dp.register_message_handler(respondent_show_answers, state=RespondentStates.show_answers)

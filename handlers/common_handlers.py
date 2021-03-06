"""Common handlers."""

# Libraries, classes and functions imports
import asyncio
import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from data import db_session
from data.QuestionModel import Question
from data.UserModel import User
from handlers.common_user_handlers import common_user_send_actions, common_user_send_interactions
from handlers.respondent_handlers import respondent_send_actions, respondent_send_interactions
from handlers.states import QuizStates, RespondentStates, CommonUserStates, AskQuestionStates, FindQuestionStates, \
    CommonStates

logger = logging.getLogger(__name__)

# Keyboards.
keyboard_for_quiz = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buttons = [
    types.KeyboardButton(text="Give me this test!"),
    types.KeyboardButton(text="I prefer to do it later...")
]
keyboard_for_quiz.add(*buttons)
is_answered_signs = ['❌', '✅']

to_main_menu_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
to_main_menu_kb.add(types.KeyboardButton(text="Back to menu ↩️🥺"))

# Creating session for db.
session = db_session.create_session()


async def cmd_start(message: types.Message, state: FSMContext):
    """Function triggers on /start."""

    logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) sent /start command.")
    await state.finish()
    user = session.query(User).get(message.from_user.id)
    if user:
        await message.answer(text="Hi! Nice to see you again")
        await CommonStates.to_main_menu.set()
        await send_user_to_main_menu(message, state)
    else:
        user = User(
            id=message.from_user.id,
            chat_id=message.chat.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            rating=0
        )
        session.add(user)
        session.commit()
        logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) successfully registered.")
        user_name = message.from_user.first_name + ' ' + message.from_user.last_name \
            if message.from_user.last_name else message.from_user.first_name
        await message.answer(text=f"Hi 👋🏼 {user_name}!!!\n"
                                  f"You successfully registered and you have access to the questions database🎉🎉🎉\n\n"
                                  f"However, in order to answer on the questions and earn Innopoints you have to pass"
                                  f" a fascinating test to determine your competence in different spheres of Innopolis.",
                             reply_markup=keyboard_for_quiz)
        await QuizStates.wait_for_reply.set()


async def cmd_help(message: types.Message):
    """Function triggers on /help."""

    logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) sent /help command.")
    await CommonStates.help.set()
    await message.answer(text="It’s an up-to-date Bot with a database of questions that were answered with competent "
                              "answers. You always can contact developer:\n"
                              "📩: l.rekhlov@innopolis.university\n"
                              "📩: s.kamalov@innopolis.university\n"
                              "telegram: @RRMOLL\n", reply_markup=to_main_menu_kb)


async def cmd_rules(message: types.Message):
    """Function triggers on /rules."""

    logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) sent /rules command.")
    await CommonStates.rules.set()
    await message.answer(text=f"-How to use Q&A Bot?\n"
                              f"-It's so easy in using\n\n"
                              f"🤴🏼 Main rules for users:\n\n"
                              f"1. If you want to find a question in data base:\n"
                              f"    - You need to send #Hashtags, which describe your question 🙋 \n"
                              f"    - After, you get some questions with the same #Hashtags \n"
                              f"    - Next, you can flip questions over by ⬅️➡️\n\n"
                              f"2. If you want to create your question:\n"
                              f"    - You need to send the question\n"
                              f"    - After, send all #Hashtags in one message\n"
                              f"    - Next, you need only wait...\n\n"
                              f"3. If you want to check your questions:\n"
                              f"    - You need to press the 'Interaction' button\n"
                              f"    - Next, press the 'My questions' button\n\n"
                              f"4. If you want to request an anonymous chat about any question:\n"
                              f"    - You need to choose question about which you want to request a chat\n"
                              f"    - After, press the 'Show answer' and 'Request'\n\n"
                              f"👨🏽‍💻 Additional rules for respondent:\n\n"
                              f"1. If you want to check your answers:\n"
                              f"    - You need to press the 'Interaction' button\n"
                              f"    - Next, press the 'My answers' button\n\n"
                              f"2. If you want to answer on available questions:\n"
                              f"    - You need to press the 'Interaction' button\n"
                              f"    - Next, press the 'Available questions' button\n\n"
                              f"3. If you get request on anonymous chat:\n"
                              f"    - You need to press the 'Interaction' button\n"
                              f"    - Next, press the 'Requests' button\n",
                         reply_markup=to_main_menu_kb)


async def send_user_to_main_menu(message: types.Message, state: FSMContext):
    """Sends user to main menu."""

    logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) is in main menu now.")
    user = session.query(User).get(message.from_user.id)
    if not user:
        logger.error(msg=f"Can't get user {message.from_user.first_name}(@{message.from_user.username})")
        await message.answer(text="Oops, something went wrong :(",
                             reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:
        stat = user.is_respondent
        if stat in [0, 1, 2]:
            await CommonUserStates.send_actions.set()
            await common_user_send_actions(message)
        elif stat == 3:
            await RespondentStates.send_actions.set()
            await respondent_send_actions(message)


async def react_to_actions(message: types.Message, state: FSMContext):
    """Different reactions to actions."""

    text = message.text
    if text == "Interaction":
        logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) opened Interaction menu.")
        user = session.query(User).get(message.from_user.id)
        if not user:
            logger.error(msg=f"Can't find user {message.from_user.first_name}(@{message.from_user.username}).")
            await message.answer(text="Oops, something went wrong :(",
                                 reply_markup=types.ReplyKeyboardRemove())
            await state.finish()
            return

        stat = user.is_respondent
        if stat in [0, 1, 2]:
            await CommonUserStates.send_interactions.set()
            await common_user_send_interactions(message)
        elif stat == 3:
            await RespondentStates.send_interactions.set()
            await respondent_send_interactions(message)

    if text == "Ask question":
        logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) asking a question.")
        await message.answer(text="Goood choice👍 Please send me your question⁉️:",
                             reply_markup=types.ReplyKeyboardRemove())
        await AskQuestionStates.getting_question.set()
    elif text == "Find question":
        logger.info(msg=f"User {message.from_user.first_name}(@{message.from_user.username}) finding a question.")
        await message.answer("So goood 👍 Send me hashtags, which describe your question:",
                             reply_markup=types.ReplyKeyboardRemove())
        await FindQuestionStates.getting_hashtags.set()


async def show_questions(message: types.Message, state: FSMContext):
    """Showing user's questions."""

    await state.reset_data()
    await message.bot.unpin_all_chat_messages(chat_id=message.chat.id)
    questions = session.query(Question).filter(Question.from_user_id == message.from_user.id).all()
    size = len(questions)
    if size:
        logger.info(msg=f"Showing user's {message.from_user.first_name}(@{message.from_user.username}) questions.")
        buttons = [
            [types.InlineKeyboardButton(text='⬅️', callback_data="previous_question"),
             types.InlineKeyboardButton(text=f'1/{size}', callback_data="question_num"),
             types.InlineKeyboardButton(text='➡️', callback_data="next_question")]
        ]
        if questions[0].is_answered:
            buttons.append([types.InlineKeyboardButton(text="Show answer", callback_data="show_answer")])
        buttons.append([types.InlineKeyboardButton(text="Back to menu ↩️🥺", callback_data="go_back")])
        showing_questions_keyboard = types.InlineKeyboardMarkup(row_width=3)
        showing_questions_keyboard.inline_keyboard = buttons
        await state.update_data(index=0, questions=questions, message=message, show_answer=False,
                                request_sent=False)
        await message.answer(text="Your questions 🧐:", reply_markup=types.ReplyKeyboardRemove())
        await message.answer(text=f"Question:\n"
                                  f"{questions[0].text}\n\n"
                                  f"Answered: {is_answered_signs[questions[0].is_answered]}",
                             reply_markup=showing_questions_keyboard)
        await CommonStates.show_questions.set()
    else:
        await message.answer(text="Sorry, but there are no questions.")
        await asyncio.sleep(0.5)
        user = session.query(User).get(message.from_user.id)
        if user.is_respondent in [0, 1, 2]:
            await CommonUserStates.send_interactions.set()
            await common_user_send_interactions(message)
        else:
            await RespondentStates.send_interactions.set()
            await respondent_send_interactions(message)


def register_common_handlers(dp: Dispatcher):
    """Registers all common_handlers to dispatcher."""

    logger.info(msg=f"Registering common handlers.")
    dp.register_message_handler(cmd_start, commands='start', state="*")
    dp.register_message_handler(cmd_help, commands='help', state='*')
    dp.register_message_handler(cmd_rules, commands="rules", state='*')
    dp.register_message_handler(react_to_actions, state=CommonStates.react_to_actions)
    dp.register_message_handler(send_user_to_main_menu, state=CommonStates.to_main_menu)
    dp.register_message_handler(send_user_to_main_menu,
                                Text(equals="Back to menu ↩️🥺"), state=RespondentStates.react_to_inters)
    dp.register_message_handler(send_user_to_main_menu,
                                Text(equals="Back to menu ↩️🥺"), state=CommonUserStates.react_to_inters)
    dp.register_message_handler(send_user_to_main_menu,
                                Text(equals="Back to menu ↩️🥺"), state=CommonStates.rules)
    dp.register_message_handler(send_user_to_main_menu,
                                Text(equals="Back to menu ↩️🥺"), state=CommonStates.help)
    dp.register_message_handler(show_questions, Text(equals="My questions"),
                                state=CommonUserStates.react_to_inters)
    dp.register_message_handler(show_questions, Text(equals="My questions"),
                                state=RespondentStates.react_to_inters)
    dp.register_message_handler(show_questions, state=CommonStates.show_questions)

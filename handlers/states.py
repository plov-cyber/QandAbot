"""All states needed for Finite-State Machine."""

# Imports
from aiogram.dispatcher.filters.state import State, StatesGroup


class CommonStates(StatesGroup):
    """Common states."""

    react_to_actions = State()
    show_questions = State()
    to_main_menu = State()
    load_questions = State()


class QuizStates(StatesGroup):
    """Quiz states."""

    wait_for_reply = State()
    passing_quiz = State()


class RespondentStates(StatesGroup):
    """Respondent states."""

    wait_for_reply = State()
    send_actions = State()
    send_interactions = State()
    react_to_inters = State()


class CommonUserStates(StatesGroup):
    """States for simple user."""

    send_actions = State()
    send_interactions = State()
    react_to_inters = State()


class FindQuestionStates(StatesGroup):
    """States for finding questions."""

    getting_hashtags = State()
    show_questions = State()


class AskQuestionStates(StatesGroup):
    """States for asking questions."""

    getting_question = State()
    getting_hashtags = State()

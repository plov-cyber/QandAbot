"""All states needed for Finite-State Machine."""

# Imports
from aiogram.dispatcher.filters.state import State, StatesGroup


class QuizStates(StatesGroup):
    """Quiz states."""

    wait_for_reply = State()


class RespondentStates(StatesGroup):
    """Respondent states."""

    wait_for_reply = State()
    send_actions = State()
    react_to_actions = State()


class CommonUserStates(StatesGroup):
    """States for simple user."""

    send_actions = State()
    react_to_actions = State()


class FindQuestionStates(StatesGroup):
    """States for finding questions."""

    getting_hashtags = State()


class AskQuestionStates(StatesGroup):
    """States for asking questions."""

    getting_question = State()
    getting_hashtags = State()

"""All states needed for Finite-State Machine."""

# Imports
from aiogram.dispatcher.filters.state import State, StatesGroup


class QuizStates(StatesGroup):
    """Quiz states."""

    wait_for_reply = State()


class RespondentStates(StatesGroup):
    """Respondent states."""

    wait_for_reply = State()

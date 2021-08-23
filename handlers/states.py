from aiogram.dispatcher.filters.state import State, StatesGroup


# Quiz
class QuizStates(StatesGroup):
    wait_for_reply = State()
    quiz = State()


# Become a respondent
class RespondentStates(StatesGroup):
    wait_for_reply = State()

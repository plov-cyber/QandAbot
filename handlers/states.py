from aiogram.dispatcher.filters.state import State, StatesGroup

wait_for_question = State()
find_question = State()

# Quiz
class QuizStates(StatesGroup):
    wait_for_reply = State()
    quiz = State()

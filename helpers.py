"""Help functions."""

# imports
from data import db_session
from data.QuestionModel import Question

session = db_session.create_session()


def find_questions_by_hashtags(hashtags):
    """Finds questions by hashtags."""

    questions = session.query(Question).all()
    suit_questions = []
    for q in questions:
        q_hashs = [h.text for h in q.hashtags]
        suit_hashtags = list(set(q_hashs) & set(hashtags))
        if suit_hashtags:
            suit_questions.append((q, len(suit_hashtags)))
    suit_questions = list(map(lambda x: x[0], sorted(suit_questions, key=lambda x: x[1])))  # list of questions
    return suit_questions

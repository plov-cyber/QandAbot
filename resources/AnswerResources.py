"""Resources for Answer."""

# Libraries, classes and functions imports
from flask_restful import Resource, abort, reqparse

from data import db_session
from data.AnswerModel import Answer

# Arguments parser
parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('text', type=str)
parser.add_argument('from_user_id', type=int)


def abort_if_answer_not_found(answer_id):
    """Function to check if answer exists."""

    session = db_session.create_session()
    answer = session.query(Answer).get(answer_id)
    if not answer:
        abort(404, message=f"Answer {answer_id} is not found.")


def abort_if_answer_already_exists(answer_text):
    """Function to check if answer already exists."""

    session = db_session.create_session()
    answer = session.query(Answer).filter(Answer.text == answer_text).all()
    if answer:
        abort(404, message=f"Answer \"{answer[0].text}\" already exists.")


class AnswerResource(Resource):
    """Resource to ..."""  # write

    pass


class AnswersListResource(Resource):
    """Resource to ..."""  # write

    pass

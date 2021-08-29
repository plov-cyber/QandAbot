"""Resources for Question."""

# Libraries, classes and functions imports
from flask import jsonify
from flask_restful import Resource, abort, reqparse

from data import db_session
from data.QuestionModel import Question

# Arguments parser
parser = reqparse.RequestParser()
parser.add_argument('text', type=str)
parser.add_argument('is_answered', type=bool)
parser.add_argument('from_user_id', type=int)


def abort_if_question_not_found(question_id):
    """Function to check if question exists."""

    session = db_session.create_session()
    question = session.query(Question).get(question_id)
    if not question:
        abort(404, message=f"Question {question_id} is not found.")


def abort_if_question_already_exists(question_text):
    """Function to check if question already exists."""

    session = db_session.create_session()
    question = session.query(Question).filter(Question.text == question_text).all()
    if question:
        abort(404, message=f"Question \"{question[0].text}\" already exists.")


class QuestionResource(Resource):
    """Resource to ..."""  # write

    pass


class QuestionsListResource(Resource):
    """Resource to get all questions, add new question, ..."""  # write

    def get(self):
        """Get all questions."""

        session = db_session.create_session()
        questions = session.query(Question).all()
        return jsonify(
            {'questions': [item.to_dict(only=['text', 'is_answered', 'from_user_id']) for item in questions]}
        )

    def post(self):
        """Add new question."""

        args = parser.parse_args()
        abort_if_question_already_exists(args['text'])
        session = db_session.create_session()
        question = Question(
            text=args['text'],
            is_answered=args['is_answered'],
            from_user_id=args['from_user_id']
        )
        session.add(question)
        session.commit()
        return jsonify({'success': 'OK'})

"""Resource for Hashtag."""

# Libraries, classes and functions imports
from flask import jsonify
from flask_restful import Resource, abort, reqparse

from data import db_session
from data.HashtagModel import Hashtag
# Arguments parser
from data.QuestionModel import Question

parser = reqparse.RequestParser()
parser.add_argument('text', type=str)
parser.add_argument('question', type=str)


def abort_if_hashtag_not_found(hashtag_id):
    """Function to check if hashtag exists."""

    session = db_session.create_session()
    hashtag = session.query(Hashtag).get(hashtag_id)
    if not hashtag:
        abort(404, msg=f"Hashtag {hashtag_id} is not found.")


def abort_if_hashtag_already_exists(hashtag_text):
    """Function to check if hashtag already exists."""

    session = db_session.create_session()
    hashtag = session.query(Hashtag).filter(Hashtag.text == hashtag_text).all()
    if hashtag:
        abort(404, message=f"hashtag \"{hashtag[0].text}\" already exists.")


class HashtagResource(Resource):
    """Resource to ..."""  # write

    pass


class HashtagsListResource(Resource):
    """Resource to add new hashtag, ..."""  # write

    def post(self):
        """Add new hashtag"""

        args = parser.parse_args()
        session = db_session.create_session()
        hashtag = session.query(Hashtag).filter(Hashtag.text == args['text']).all()
        if not hashtag:
            hashtag = Hashtag(
                text=args['text']
            )
            session.add(hashtag)
        else:
            hashtag = hashtag[0]
        question = session.query(Question).filter(Question.text == args['question']).all()
        if question:
            hashtag.questions.append(question[0])
        session.commit()
        return jsonify({'success': 'OK'})



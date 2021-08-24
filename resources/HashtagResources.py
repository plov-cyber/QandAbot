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
        abort_if_hashtag_already_exists(args['text'])
        session = db_session.create_session()
        hashtag = Hashtag(
            text=args['text']
        )
        question = session.query(Question).filter(Question.text == args['question'])
        if question:
            question = question[0]
            question.hashtags.append(hashtag)
            session.merge(question)
        session.add(hashtag)
        session.commit()
        return jsonify({'success': 'OK'})



"""Resource for Hashtag."""

# Libraries, classes and functions imports
from flask import jsonify
from flask_restful import Resource, abort, reqparse
from data import db_session
from data.HashtagModel import Hashtag

# Arguments parser
parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('hashtag', type=str)


def abort_if_hashtag_not_found(hashtag_id):
    """Function to check if hashtag exists."""

    session = db_session.create_session()
    hashtag = session.query(Hashtag).get(hashtag_id)
    if not hashtag:
        abort(404, msg=f"Hashtag {hashtag_id} is not found.")


class HashtagResource(Resource):
    """Resource to ..."""  # write

    pass


class HashtagsListResource(Resource):
    """Resource to ..."""  # write

    pass

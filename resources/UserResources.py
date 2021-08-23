"""Resources for User."""

# Libraries, classes and functions imports
from flask import jsonify
from flask_restful import Resource, abort, reqparse
from data import db_session
from data.UserModel import User

# Arguments parser
parser = reqparse.RequestParser()
parser.add_argument('id', type=int, required=True)
parser.add_argument('username', type=str, required=True)
parser.add_argument('first_name', type=str, required=True)
parser.add_argument('last_name', type=str)


def abort_if_user_not_found(user_id):
    """Function to check if user exists."""

    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} is not found.")


class UserResource(Resource):
    """Resource to get and delete user, change user's data."""  # add another later

    def get(self, user_id):
        """Get single user."""

        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict()})

    def put(self, user_id):
        """Change user's data."""

        args = parser.parse_args()
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        user.is_respondent = args['is_respondent']
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, user_id):
        """Delete all user's data."""

        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    """Resource to get all users, post new users."""  # add another later

    def get(self):
        """Get all users."""

        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify(
            {'users': [item.to_dict() for item in users]}
        )

    def post(self):
        """Add new user."""

        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            id=args['id'],
            username=args['username'],
            first_name=args['first_name'],
            last_name=args['last_name']
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})

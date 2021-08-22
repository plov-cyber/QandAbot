from flask import jsonify
from flask_restful import Resource, abort, reqparse
from data import db_session
from data.UserModel import User

parser = reqparse.RequestParser()
parser.add_argument('id', type=int, required=True)
parser.add_argument('username', type=str, required=True)
parser.add_argument('first_name', type=str, required=True)
parser.add_argument('last_name', type=str)


class UsersListResource(Resource):
    def post(self):
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

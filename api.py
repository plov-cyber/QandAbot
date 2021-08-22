import os
from flask import Flask
from flask_restful import Api

from data import db_session
from resources.UserResources import UsersListResource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some_secret_key'

db_session.global_init('db/data.sqlite')

api = Api(app)
# api.add_resource(UserResource, '/api_users/<int:user_id>')
api.add_resource(UsersListResource, '/api_users')

PORT = int(os.environ.get("PORT", 80))

if __name__ == '__main__':
    app.run('0.0.0.0', port=PORT)
    os.remove('db/data.sqlite')

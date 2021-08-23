"""API file. Creates database and app. Starts the server."""

# Libraries, classes and functions imports
import os

from flask import Flask
from flask_restful import Api

from config import SECRET_KEY
from data import db_session
from resources.UserResources import UsersListResource, UserResource

# Creating app
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
PORT = int(os.environ.get("PORT", 80))

# Initializing database
db_session.global_init('db/data.sqlite')

# Creating api and adding resources
api = Api(app)
api.add_resource(UserResource, '/api_users/<int:user_id>')
api.add_resource(UsersListResource, '/api_users')

if __name__ == '__main__':
    app.run('0.0.0.0', port=PORT)
    os.remove('db/data.sqlite')

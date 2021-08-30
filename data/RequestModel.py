# Libraries, classes and functions imports
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Request(SqlAlchemyBase, SerializerMixin):
    """Request model for database."""

    __tablename__ = 'requests'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, index=True)
    from_user_id = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=False)
    to_user_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey('users.id'))
    question_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey('questions.id'))
    to_user = orm.relation('User')
    question = orm.relation('Question')

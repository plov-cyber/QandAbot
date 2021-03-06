# Libraries, classes and functions imports
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, SerializerMixin):
    """User model for database."""

    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True, index=True)
    chat_id = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=False)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    first_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    last_name = sqlalchemy.Column(sqlalchemy.String)
    rating = sqlalchemy.Column(sqlalchemy.Float)
    is_respondent = sqlalchemy.Column(sqlalchemy.SmallInteger, nullable=False, default=0)
    questions = orm.relation('Question', back_populates='from_user')
    answers = orm.relation('Answer', back_populates='from_user')
    requests = orm.relation('Request', back_populates='to_user')

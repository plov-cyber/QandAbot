# Libraries, classes and functions imports
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, SerializerMixin):
    """User model for database."""

    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True, index=True)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    first_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    last_name = sqlalchemy.Column(sqlalchemy.String)
    is_respondent = sqlalchemy.Column(sqlalchemy.SmallInteger, nullable=False, default=0)

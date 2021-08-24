# Libraries, classes and functions imports
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Hashtag(SqlAlchemyBase, SerializerMixin):
    """Hashtag model for database."""

    __tablename__ = 'hashtags'

    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True, index=True, autoincrement=True)
    hashtag = sqlalchemy.Column(sqlalchemy.String, nullable=False)

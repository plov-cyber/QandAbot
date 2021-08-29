# Libraries, classes and functions imports
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Hashtag(SqlAlchemyBase, SerializerMixin):
    """Hashtag model for database."""

    __tablename__ = 'hashtags'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)


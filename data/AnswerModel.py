# Libraries, classes and functions imports
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Answer(SqlAlchemyBase, SerializerMixin):
    """Answer model for database."""

    __tablename__ = 'answers'

    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True, index=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    from_user_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey('users.id'))
    from_user = orm.relation('User')
    question = orm.relation('Question', back_populates='answer')

# Libraries, classes and functions imports
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Question(SqlAlchemyBase, SerializerMixin):
    """Question model for database."""

    __tablename__ = 'questions'

    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True, index=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    is_answered = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    from_user_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey('users.id'))
    from_user = orm.relation('User')
    answer = orm.relation('Answer', back_populates='question')

# Libraries, classes and functions imports
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase

question_to_hashtag = sqlalchemy.Table('question_to_hashtag', SqlAlchemyBase.metadata,
                                       sqlalchemy.Column('question', sqlalchemy.BigInteger,
                                                         sqlalchemy.ForeignKey('questions.id'), primary_key=True),
                                       sqlalchemy.Column('hashtag', sqlalchemy.BigInteger,
                                                         sqlalchemy.ForeignKey('hashtags.id'), primary_key=True))


class Question(SqlAlchemyBase, SerializerMixin):
    """Question model for database."""

    __tablename__ = 'questions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, index=True)
    text = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    is_answered = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=0)
    from_user_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey('users.id'))
    from_user = orm.relation('User')
    answers = orm.relation('Answer', back_populates='question')
    hashtags = orm.relation('Hashtag', secondary='question_to_hashtag', backref='questions')

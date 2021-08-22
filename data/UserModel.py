import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True, index=True)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    first_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    last_name = sqlalchemy.Column(sqlalchemy.String)
    is_specialist = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)

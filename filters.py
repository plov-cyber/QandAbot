from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

from data import db_session
from data.UserModel import User


class FirstTimeFilter(BoundFilter):
    key = 'first_time'

    def __init__(self, first_time):
        self.first_time = first_time

    async def check(self, message: types.Message):
        session = db_session.create_session()
        user = session.query(User).get(message.from_user.id)
        return False if user else True

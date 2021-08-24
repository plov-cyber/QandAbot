"""Common callbacks."""

# imports
import logging

from aiogram import types, Dispatcher

logger = logging.getLogger(__name__)


async def some_function(callback: types.CallbackQuery):
    """Some description."""

    # start coding from here


def register_common_callbacks(dp: Dispatcher):
    """Registers all common callbacks to dispatcher."""

    logger.info(msg="Registering common callbacks.")
    dp.register_callback_query_handler(some_function)

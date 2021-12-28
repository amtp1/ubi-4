from aiogram.dispatcher.filters.state import StatesGroup, State

class Attack(StatesGroup):
    set_phone_call = State()

class Mailing(StatesGroup):
    set_mailing_text_call = State()
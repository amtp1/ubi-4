from aiogram.dispatcher.filters.state import StatesGroup, State

class Attack(StatesGroup):
    set_symbol = State()
    set_phone_call = State()
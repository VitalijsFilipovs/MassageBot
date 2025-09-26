# bot/states.py
from aiogram.fsm.state import StatesGroup, State

class Onboarding(StatesGroup):
    lang = State()
    role = State()
    provider_gender = State()
    client_gender = State()
    choose_city = State()
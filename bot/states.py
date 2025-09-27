# bot/states.py
from aiogram.fsm.state import StatesGroup, State

class Onboarding(StatesGroup):
    lang = State()
    role = State()
    provider_gender = State()
    client_gender = State()
    choose_city = State()

class ProviderReg(StatesGroup):
    name = State()
    city = State()
    about = State()
    price = State()
    phone = State()           # <— новый шаг
    phone_vis = State()       # <— показать/скрыть
    photos = State()
    confirm = State()
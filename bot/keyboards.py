# bot/keyboards.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from .i18n import t, Lang

def lang_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text="RU 🇷🇺", callback_data="lang:ru"),
         InlineKeyboardButton(text="LV 🇱🇻", callback_data="lang:lv"),
         InlineKeyboardButton(text="EN 🇬🇧", callback_data="lang:en")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def role_keyboard(lang: Lang) -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text=t("role_provider", lang), callback_data="role:provider")],
        [InlineKeyboardButton(text=t("role_client", lang),   callback_data="role:client")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def gender_keyboard(lang: Lang) -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text=t("gender_female", lang), callback_data="gender:female"),
         InlineKeyboardButton(text=t("gender_male", lang),   callback_data="gender:male")],
        [InlineKeyboardButton(text=t("gender_other", lang),  callback_data="gender:other")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def share_contact_keyboard(lang: Lang) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[[KeyboardButton(text=t("share_contact", lang), request_contact=True)]],
    )

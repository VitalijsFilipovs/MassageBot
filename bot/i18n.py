# bot/i18n.py
from typing import Literal

Lang = Literal["ru", "lv", "en"]

TEXTS = {
    "start_choose_lang": {
        "ru": "Выберите язык:",
        "lv": "Izvēlieties valodu:",
        "en": "Choose your language:",
    },
    "start_choose_role": {
        "ru": "Кто вы?",
        "lv": "Kas jūs esat?",
        "en": "Who are you?",
    },
    "role_provider": {"ru": "Я делаю массаж", "lv": "Es sniedzu masāžu", "en": "I provide massage"},
    "role_client":   {"ru": "Мне нужен массаж", "lv": "Man vajag masāžu", "en": "I need a massage"},

    "choose_gender": {
        "ru": "Укажите пол:",
        "lv": "Norādiet dzimumu:",
        "en": "Select your gender:",
    },
    "gender_female": {"ru": "Я женщина", "lv": "Sieviete", "en": "Female"},
    "gender_male":   {"ru": "Я мужчина", "lv": "Vīrietis", "en": "Male"},
    "gender_other":  {"ru": "Другое", "lv": "Cits", "en": "Other"},

    "provider_known": {
        "ru": "С возвращением! Ваш профиль найден. Открыть меню мастера?",
        "lv": "Laipni lūgti atpakaļ! Jūsu profils ir atrasts. Atvērt meistara izvēlni?",
        "en": "Welcome back! Your profile was found. Open provider menu?",
    },
    "provider_register": {
        "ru": "Давайте зарегистрируем профиль массажистки. Поделиться контактом?",
        "lv": "Reģistrēsim masieres profilu. Dalīties ar kontaktu?",
        "en": "Let's register your provider profile. Share contact?",
    },
    "share_contact": {
        "ru": "Поделиться контактом",
        "lv": "Dalīties ar kontaktu",
        "en": "Share contact",
    },
    "client_choose_gender": {
        "ru": "Предпочтительный пол массажиста:",
        "lv": "Vēlamais masiera dzimums:",
        "en": "Preferred therapist gender:",
    },
    "choose_city": {
        "ru": "Выберите город:",
        "lv": "Izvēlieties pilsētu:",
        "en": "Choose a city:",
    },
    "no_profiles": {
        "ru": "Пока нет анкет по выбранным параметрам.",
        "lv": "Pašlaik nav profilu ar šiem parametriem.",
        "en": "No profiles match your filters yet.",
    },
    "view_more": {
        "ru": "Подробнее",
        "lv": "Sīkāk",
        "en": "Details",
    },
}

def t(key: str, lang: Lang = "ru") -> str:
    block = TEXTS.get(key, {})
    return block.get(lang, block.get("ru", key))

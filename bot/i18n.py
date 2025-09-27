# bot/i18n.py
from typing import Literal

Lang = Literal["ru", "lv", "en"]

TEXTS = {
        "greeting": {
        "ru": "👋 Добро пожаловать в MassageBot!\nЯ помогу найти мастера или опубликовать профиль.",
        "lv": "👋 Laipni lūgti MassageBot!\nPalīdzu atrast masieri vai publicēt profilu.",
        "en": "👋 Welcome to MassageBot!\nI'll help you find a masseuse or publish your profile.",
    },
    "lang_set": {
        "ru": "Язык переключён на русский.",
        "lv": "Valoda iestatīta uz latviešu.",
        "en": "Language switched to English.",
    },
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

    # регистрация
    "reg_name":  {"ru": "Как вас представлять в анкете? (Имя/псевдоним)",
                  "lv": "Kā jūs saukt profilā?", "en":"How should we show your name?"},
    "reg_city":  {"ru": "Выберите город:", "lv":"Izvēlieties pilsētu:", "en":"Choose your city:"},
    "reg_about": {"ru": "Коротко о себе и услугах (можно пропустить кнопкой «Пропустить»).",
                  "lv":"Īsi par sevi un pakalpojumiem (var izlaist).",
                  "en":"Tell about you (or Skip)."},
    "reg_price": {"ru": "Укажите цену «от», € (например: 40). Можно пропустить.",
                  "lv":"Norādiet cenu „no”, € (piem.: 40). Var izlaist.",
                  "en":"Enter price from, € (e.g. 40). You can skip."},

    # телефон (необязательный)
    "reg_phone": {"ru": "Оставьте номер телефона (необязательно). Формат: +371xxxxxxxx",
                  "lv":"Norādiet tālruni (nav obligāti). Formāts: +371xxxxxxx",
                  "en":"Add your phone (optional). Format: +371xxxxxxx"},
    "ask_show_phone": {"ru":"Показывать телефон в анкете?",
                       "lv":"Rādīt tālruni profilā?", "en":"Show phone on your profile?"},
    "show_yes": {"ru":"Да, показывать", "lv":"Jā, rādīt", "en":"Yes, show"},
    "show_no":  {"ru":"Нет, скрыть",   "lv":"Nē, slēpt", "en":"No, hide"},

    # фото и завершение
    "reg_photos": {"ru":"Пришлите 1–3 фото (по одному). Когда готово — нажмите «Готово».",
                   "lv":"Sūtiet 1–3 foto. Kad gatavs — nospiediet “Gatavs”.",
                   "en":"Send 1–3 photos. Then press “Done”."},
    "skip": {"ru":"Пропустить","lv":"Izlaist","en":"Skip"},
    "done": {"ru":"Готово","lv":"Gatavs","en":"Done"},
    "preview_title": {"ru":"Проверьте анкету:",
                      "lv":"Pārbaudiet profilu:", "en":"Preview your profile:"},
    "preview_publish": {"ru":"Отправить на модерацию",
                        "lv":"Iesniegt moderācijai", "en":"Submit for review"},
    "preview_edit": {"ru":"Изменить","lv":"Labot","en":"Edit"},
    "saved_pending": {"ru":"✅ Анкета отправлена на модерацию. Мы сообщим, когда её одобрят.",
                      "lv":"✅ Profils iesniegts moderācijai.","en":"✅ Profile submitted for review."},

    # инфо о подписке
    "fee_note": {
        "ru":"ℹ️ Публикация анкеты и показ в поиске — по подписке **€10/мес**. Оплатить можно позже.",
        "lv":"ℹ️ Profila publicēšana un meklēšana — ar abonementu **€10/mēn**. Var samaksāt vēlāk.",
        "en":"ℹ️ Publishing your profile in search requires a **€10/mo** subscription. You can pay later.",
    },
    "fee_warn": {
        "ru":"⚠️ Публикация потребует активной подписки (€10/мес).",
        "lv":"⚠️ Publicēšanai būs nepieciešams aktīvs abonements (€10/mēn).",
        "en":"⚠️ Publishing requires an active €10/mo subscription.",
    },
}

def t(key: str, lang: Lang = "ru") -> str:
    block = TEXTS.get(key, {})
    return block.get(lang, block.get("ru", key))

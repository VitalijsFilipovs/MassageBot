# bot/routers/onboarding.py
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from ..i18n import t, Lang
from ..keyboards import lang_keyboard, role_keyboard, gender_keyboard, share_contact_keyboard
from ..states import Onboarding
from .. import api

router = Router()

DEFAULT_LANG: Lang = "ru"

def get_lang(data: dict) -> Lang:
    return data.get("lang", DEFAULT_LANG)

@router.message(CommandStart())
async def cmd_start(m: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Onboarding.lang)
    await m.answer(t("start_choose_lang", DEFAULT_LANG), reply_markup=lang_keyboard())

@router.callback_query(F.data.startswith("lang:"))
async def cb_lang(c: CallbackQuery, state: FSMContext):
    lang = c.data.split(":", 1)[1]  # ru|lv|en
    await state.update_data(lang=lang)
    # завести/обновить пользователя в API
    await api.get_or_create_user(tg_id=c.from_user.id, locale=lang)
    await state.set_state(Onboarding.role)
    await c.message.edit_text(t("start_choose_role", lang))
    await c.message.edit_reply_markup(reply_markup=role_keyboard(lang))  # показать роли
    await c.answer()

@router.callback_query(F.data.startswith("role:"))
async def cb_role(c: CallbackQuery, state: FSMContext):
    role = c.data.split(":", 1)[1]  # provider|client
    data = await state.get_data()
    lang = get_lang(data)

    # сохранить роль у пользователя
    await api.update_user(tg_id=c.from_user.id, role=role)

    if role == "provider":
        # если уже есть профиль — сразу приветствие
        if await api.provider_exists(tg_id=c.from_user.id):
            await c.message.edit_text(t("provider_known", lang))
            await c.message.edit_reply_markup()  # убрать кнопки
        else:
            # спросим пол и предложим поделиться контактом
            await state.set_state(Onboarding.provider_gender)
            await c.message.edit_text(t("choose_gender", lang))
            await c.message.edit_reply_markup(reply_markup=gender_keyboard(lang))
    else:
        # клиент: спросим предпочтительный пол массажиста
        await state.set_state(Onboarding.client_gender)
        await c.message.edit_text(t("client_choose_gender", lang))
        await c.message.edit_reply_markup(reply_markup=gender_keyboard(lang))
    await c.answer()

@router.callback_query(Onboarding.provider_gender, F.data.startswith("gender:"))
async def cb_provider_gender(c: CallbackQuery, state: FSMContext):
    gender = c.data.split(":", 1)[1]  # female|male|other
    data = await state.get_data()
    lang = get_lang(data)
    await api.update_user(tg_id=c.from_user.id, gender=gender)

    # предложить шаринг контакта (для верификации/связи)
    await c.message.answer(t("provider_register", lang), reply_markup=share_contact_keyboard(lang))
    await c.answer()

@router.message(Onboarding.provider_gender, F.contact)
async def got_provider_contact(m: Message, state: FSMContext):
    data = await state.get_data()
    lang = get_lang(data)
    if not m.contact or not m.contact.phone_number:
        await m.answer("Нет телефона в контакте.")
        return
    phone = m.contact.phone_number
    # Сохраняем телефон, но по умолчанию НЕ публикуем
    await api.update_user(tg_id=m.from_user.id, phone=phone, share_phone_publicly=False)
    # дальше — переход в мастер регистрации профиля (сцены /profile) — подключим отдельным роутером
    await m.answer("Спасибо! Переходим к заполнению профиля. Команда: /profile", reply_markup=None)
    await state.clear()

@router.callback_query(Onboarding.client_gender, F.data.startswith("gender:"))
async def cb_client_gender(c: CallbackQuery, state: FSMContext):
    gender = c.data.split(":", 1)[1]
    await state.update_data(client_pref_gender=gender)
    data = await state.get_data()
    lang = get_lang(data)

    # показать список городов
    cities = await api.list_cities()
    # делаем инлайн-клавиатуру с городами (первые 9, для простоты; пагинация добавим позже)
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    rows = []
    for city in cities[:9]:
        text = city.get(f"name_{lang}", city.get("name_ru", city["slug"]))
        rows.append([InlineKeyboardButton(text=text, callback_data=f"city:{city['slug']}")])
    kb = InlineKeyboardMarkup(inline_keyboard=rows)
    await c.message.edit_text(t("choose_city", lang))
    await c.message.edit_reply_markup(reply_markup=kb)
    await state.set_state(Onboarding.choose_city)
    await c.answer()

@router.callback_query(Onboarding.choose_city, F.data.startswith("city:"))
async def cb_city(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = get_lang(data)
    pref_gender = data.get("client_pref_gender")
    city_slug = c.data.split(":", 1)[1]

    profiles = await api.search_profiles(city_slug=city_slug, gender=pref_gender, locale=lang)
    if not profiles:
        await c.message.edit_text(t("no_profiles", lang))
        await c.message.edit_reply_markup()
        await c.answer()
        return

    # Покажем "короткий список" — имя, цена, 1 маленькое фото + кнопка Подробнее
    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto

    # Для краткости — отправим серию сообщений с фото
    for p in profiles[:5]:  # первые 5
        caption = f"{p.get('display_name','')}\n{p.get('about','')[:120]}..."
        btn = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=t('view_more', lang), callback_data=f"profile:{p['id']}")]
        ])
        photos = p.get("photos") or []
        if photos:
            try:
                await c.message.answer_photo(photo=photos[0], caption=caption, reply_markup=btn)
            except Exception:
                await c.message.answer(caption, reply_markup=btn)
        else:
            await c.message.answer(caption, reply_markup=btn)
    await c.answer()

@router.callback_query(F.data.startswith("profile:"))
async def cb_profile_detail(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = get_lang(data)
    prof_id = int(c.data.split(":", 1)[1])
    p = await api.get_profile(prof_id)

    lines = [p.get("display_name", "")]
    if p.get("about"):
        lines.append(p["about"])
    if p.get("price_from"):
        lines.append(f"Цена от: {p['price_from']} €")
    # телефон — только если разрешён к показу
    phone = None
    if p.get("share_phone_publicly") and p.get("phone"):
        phone = p["phone"]
        lines.append(f"Телефон: {phone}")

    text = "\n".join(lines)
    photos = p.get("photos") or []
    if photos:
        try:
            await c.message.answer_photo(photo=photos[0], caption=text)
        except Exception:
            await c.message.answer(text)
    else:
        await c.message.answer(text)

    # кнопка "написать" — t.me/username если есть, иначе просто reply
    if c.from_user.username:
        await c.message.answer(f"Написать: https://t.me/{c.from_user.username}")
    await c.answer()

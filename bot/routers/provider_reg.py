# bot/routers/provider_reg.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from ..states import ProviderReg
from ..i18n import t, Lang
from .. import api

router = Router()
DEFAULT_LANG: Lang = "ru"

def _get_lang(data: dict) -> Lang:
    return data.get("lang", DEFAULT_LANG)

def _skip_kb(lang: Lang):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=t("skip", lang), callback_data="skip")]]
    )

def _done_kb(lang: Lang):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=t("done", lang), callback_data="done")]]
    )

# 1) Имя
@router.message(ProviderReg.name, F.text)
async def reg_name(m: Message, state: FSMContext):
    name = (m.text or "").strip()
    if len(name) < 2:
        return await m.answer("Имя слишком короткое. Введите от 2 символов.")
    await state.update_data(reg_name=name)

    data = await state.get_data()
    lang = _get_lang(data)

    cities = await api.list_cities()
    rows = [[InlineKeyboardButton(
        text=city.get(f"name_{lang}", city.get("name_ru", city["slug"])),
        callback_data=f"prov_city:{city['slug']}"
    )] for city in cities[:9]]
    kb = InlineKeyboardMarkup(inline_keyboard=rows)

    await m.answer(t("choose_city", lang), reply_markup=kb)
    await state.set_state(ProviderReg.city)

# 2) Город
@router.callback_query(ProviderReg.city, F.data.startswith("prov_city:"))
async def reg_city(c: CallbackQuery, state: FSMContext):
    city_slug = c.data.split(":", 1)[1]
    await state.update_data(reg_city_slug=city_slug)

    data = await state.get_data()
    lang = _get_lang(data)

    await c.message.edit_text(t("reg_about", lang))
    await c.message.edit_reply_markup()
    await state.set_state(ProviderReg.about)
    await c.answer()

# 3) About (можно пропустить)
@router.callback_query(ProviderReg.about, F.data == "skip")
async def reg_about_skip(c: CallbackQuery, state: FSMContext):
    await state.update_data(reg_about=None)
    data = await state.get_data()
    lang = _get_lang(data)
    await state.set_state(ProviderReg.price)
    await c.message.answer(t("reg_price", lang), reply_markup=_skip_kb(lang))
    await c.answer()

@router.message(ProviderReg.about, F.text)
async def reg_about_text(m: Message, state: FSMContext):
    await state.update_data(reg_about=(m.text or "").strip()[:1000])
    data = await state.get_data()
    lang = _get_lang(data)
    await state.set_state(ProviderReg.price)
    await m.answer(t("reg_price", lang), reply_markup=_skip_kb(lang))

# 4) Цена (можно пропустить)
@router.callback_query(ProviderReg.price, F.data == "skip")
async def reg_price_skip(c: CallbackQuery, state: FSMContext):
    await state.update_data(reg_price=None)
    data = await state.get_data()
    lang = _get_lang(data)
    await state.set_state(ProviderReg.phone)
    await c.message.answer(t("reg_phone", lang), reply_markup=_skip_kb(lang))
    await c.answer()

@router.message(ProviderReg.price, F.text)
async def reg_price_text(m: Message, state: FSMContext):
    txt = (m.text or "").strip().replace(",", ".")
    price = None
    try:
        price = int(float(txt))
    except Exception:
        # пользователь мог ввести чушь — разрешим, но без цены
        price = None
    await state.update_data(reg_price=price)

    data = await state.get_data()
    lang = _get_lang(data)
    await state.set_state(ProviderReg.phone)
    await m.answer(t("reg_phone", lang), reply_markup=_skip_kb(lang))

# 5) Телефон (можно пропустить), затем «показывать телефон?»
@router.callback_query(ProviderReg.phone, F.data == "skip")
async def reg_phone_skip(c: CallbackQuery, state: FSMContext):
    await state.update_data(reg_phone=None)
    data = await state.get_data()
    lang = _get_lang(data)
    await state.set_state(ProviderReg.photos)
    await c.message.answer(t("reg_photos", lang), reply_markup=_done_kb(lang))
    await c.answer()

@router.message(ProviderReg.phone, F.text)
async def reg_phone_text(m: Message, state: FSMContext):
    raw = (m.text or "").strip().replace(" ", "")
    import re
    if not re.fullmatch(r"\+?\d{6,15}", raw):
        return await m.answer(
            "Похоже, номер в неверном формате. Пример: +37120000000\nИли нажмите «Пропустить».")
    await state.update_data(reg_phone=raw)

    data = await state.get_data()
    lang = _get_lang(data)
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=t("show_yes", lang), callback_data="vis:yes"),
        InlineKeyboardButton(text=t("show_no", lang),  callback_data="vis:no"),
    ]])
    await state.set_state(ProviderReg.phone_vis)
    await m.answer(t("ask_show_phone", lang), reply_markup=kb)

@router.callback_query(ProviderReg.phone_vis, F.data.startswith("vis:"))
async def reg_phone_vis(c: CallbackQuery, state: FSMContext):
    vis = c.data.endswith("yes")
    await state.update_data(reg_phone_vis=vis)
    data = await state.get_data()
    lang = _get_lang(data)
    await state.set_state(ProviderReg.photos)
    await c.message.answer(t("reg_photos", lang), reply_markup=_done_kb(lang))
    await c.answer()

# 6) Фото (можно несколько) → «Готово»
@router.message(ProviderReg.photos, F.photo)
async def reg_photos_collect(m: Message, state: FSMContext):
    data = await state.get_data()
    photos = list(data.get("reg_photos") or [])
    if len(photos) < 10:  # ограничим
        photos.append(m.photo[-1].file_id)
        await state.update_data(reg_photos=photos)

@router.callback_query(ProviderReg.photos, F.data == "done")
async def reg_preview(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = _get_lang(data)

    name   = data.get("reg_name")
    about  = data.get("reg_about") or ""
    price  = data.get("reg_price")
    city   = data.get("reg_city_slug")  # для простоты показываем slug
    photos = data.get("reg_photos") or []
    phone  = data.get("reg_phone")
    show   = bool(data.get("reg_phone_vis"))

    lines = [t("preview_title", lang), f"<b>{name}</b>"]
    if city: lines.append(f"city: {city}")
    if price is not None: lines.append(f"Цена от: {price} €")
    if about: lines.append(about)
    if phone and show: lines.append(f"Телефон: {phone}")
    lines.append("")
    lines.append(t("fee_warn", lang))
    text = "\n".join(lines)

    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=t("preview_publish", lang), callback_data="pub:ok"),
        InlineKeyboardButton(text=t("preview_edit", lang),    callback_data="pub:edit"),
    ]])

    if photos:
        try:
            await c.message.answer_photo(photos[0], caption=text, reply_markup=kb)
        except Exception:
            await c.message.answer(text, reply_markup=kb)
    else:
        await c.message.answer(text, reply_markup=kb)

    await state.set_state(ProviderReg.confirm)
    await c.answer()

# 7) Редактирование или публикация (создание черновика)
@router.callback_query(ProviderReg.confirm, F.data == "pub:edit")
async def reg_edit(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = _get_lang(data)
    await state.set_state(ProviderReg.name)
    await c.message.answer(t("reg_name", lang))
    await c.answer()

@router.callback_query(ProviderReg.confirm, F.data == "pub:ok")
async def reg_publish(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = _get_lang(data)

    payload = {
        "display_name": data.get("reg_name"),
        "city_slug":    data.get("reg_city_slug"),
        "about":        data.get("reg_about"),
        "price_from":   data.get("reg_price"),
        "photos":       data.get("reg_photos") or [],
        "phone":        data.get("reg_phone"),
        "share_phone_publicly": bool(data.get("reg_phone_vis")),
    }

    try:
        await api.save_profile(tg_id=c.from_user.id, payload=payload)
    except Exception:
        pass

    await c.message.answer(t("saved_pending", lang))
    await state.clear()
    await c.answer()

from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.keyboards import cancel_kb, format_kb, main_kb
from app.utils import validate_phone
from app.db import AsyncSessionLocal
from app.crud import create_lead
from app.schemas import LeadCreate
from app.config import ADMIN_CHAT_IDS

router = Router()

class Signup(StatesGroup):
    waiting_name = State()
    waiting_phone = State()
    waiting_format = State()


@router.callback_query(F.data.startswith("signup:"))
async def signup_start(query: types.CallbackQuery, state: FSMContext):
    course = query.data.split(":", 1)[1]
    await state.update_data(course=course)
    await query.message.answer(
        f"Запись на курс: <b>{course}</b>\n\nВведите ваше имя:",
        reply_markup=cancel_kb
    )
    await state.set_state(Signup.waiting_name)
    await query.answer()


# @router.message(Signup.waiting_name)
# async def signup_name(message: types.Message, state: FSMContext):
#     if message.text == "❌ Отмена":
#         await state.clear()
#         return await message.answer("Отмена записи.", reply_markup=main_kb)
#
#     await state.update_data(name=message.text.strip())
#     await message.answer("Отправьте ваш телефон :", reply_markup=cancel_kb)
#     await state.set_state(Signup.waiting_phone)
#
#
# @router.message(Signup.waiting_phone)
# async def signup_phone(message: types.Message, state: FSMContext):
#     if message.text == "❌ Отмена":
#         await state.clear()
#         return await message.answer("Отмена записи.", reply_markup=main_kb)
#
#     phone = validate_phone(message.text)
#     if not phone:
#         return await message.answer("❗ Неверный формат телефона. Попробуйте снова.")
#
#     await state.update_data(phone=phone)
#     await message.answer("Выберите формат:", reply_markup=format_kb)
#     await state.set_state(Signup.waiting_format)
from aiogram.types import KeyboardButton

# Шаг 1: ждём имя
@router.message(Signup.waiting_name)
async def signup_name(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        return await message.answer("Отмена записи.", reply_markup=main_kb)

    await state.update_data(name=message.text.strip())

    # клавиатура с кнопкой "Отправить номер"
    kb = ReplyKeyboardBuilder()
    kb.row(
        KeyboardButton(text="📱 Отправить номер", request_contact=True),
        KeyboardButton(text="❌ Отмена")
    )

    await message.answer(
        "Отправьте ваш телефон:",
        reply_markup=kb.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )
    await state.set_state(Signup.waiting_phone)


# Шаг 2: ждём телефон
@router.message(Signup.waiting_phone)
async def signup_phone(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        return await message.answer("Отмена записи.", reply_markup=main_kb)

    # ждём контакт
    if not message.contact:
        return await message.answer("❗ Пожалуйста, используйте кнопку «📱 Отправить номер».")

    phone = message.contact.phone_number  # телефон из аккаунта
    await state.update_data(phone=phone)

    await message.answer("Выберите формат:", reply_markup=format_kb)
    await state.set_state(Signup.waiting_format)


@router.message(Signup.waiting_format)
async def signup_format(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        return await message.answer("Отмена записи.", reply_markup=main_kb)

    fmt = message.text.strip()
    if fmt not in ["Онлайн", "Офлайн"]:
        return await message.answer("Пожалуйста, выберите формат через кнопки.")

    data = await state.get_data()
    await state.clear()

    payload = LeadCreate(
        name=data["name"],
        phone=data["phone"],
        course=data["course"],
        format=fmt,
        source="signup"
    )
    async with AsyncSessionLocal() as db:
        await create_lead(db, payload)

    await message.answer(
        "✅ Спасибо! Мы скоро свяжемся с вами 📞",
        reply_markup=main_kb
    )

    for admin in ADMIN_CHAT_IDS:
        await message.bot.send_message(
            admin,
            f"Новая заявка:\nИмя: {data['name']}\nТел: {data['phone']}\nКурс: {data['course']}\nФормат: {fmt}"
        )

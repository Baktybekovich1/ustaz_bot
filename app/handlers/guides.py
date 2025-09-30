from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import FSInputFile
import os

from app.config import STATIC_DIR, ADMIN_CHAT_IDS
from app.schemas import LeadCreate
from app.crud import create_lead
from app.db import AsyncSessionLocal
from app.utils import validate_phone
from app.keyboards import main_kb 

router = Router()


class GuideForm(StatesGroup):
    waiting_name = State()
    waiting_phone = State()
    waiting_email = State()


@router.message(F.text.contains("Получить бесплатный гайд"))
async def ask_guide(message: Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="Backend", callback_data="guide:backend_guide.pdf")
    kb.button(text="Frontend", callback_data="guide:frontend_guide.pdf")
    kb.adjust(1)
    await message.answer("Выберите гайд:", reply_markup=kb.as_markup())


@router.callback_query(F.data.startswith("guide:"))
async def guide_cb(query: CallbackQuery, state: FSMContext):
    filename = query.data.split(":", 1)[1]
    await state.update_data(filename=filename)
    await state.set_state(GuideForm.waiting_name)

    kb = ReplyKeyboardBuilder()
    kb.button(text="Отмена")
    await query.message.answer(
        "Введите ваше имя:",
        reply_markup=kb.as_markup(resize_keyboard=True)
    )
    await query.answer()


@router.message(GuideForm.waiting_name)
async def guide_name(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await state.clear()
        return await message.answer("Отменено.", reply_markup=main_kb)

    await state.update_data(name=message.text.strip())
    await state.set_state(GuideForm.waiting_phone)

    kb = ReplyKeyboardBuilder()
    kb.button(text="Отмена")
    await message.answer("Введите ваш телефон (в международном формате +996...):",
                         reply_markup=kb.as_markup(resize_keyboard=True))


@router.message(GuideForm.waiting_phone)
async def guide_phone(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await state.clear()
        return await message.answer("Отменено.", reply_markup=main_kb)

    phone = validate_phone(message.text)
    if not phone:
        return await message.answer("Невалидный номер. Попробуйте ещё раз (+996...).")

    await state.update_data(phone=phone)
    await state.set_state(GuideForm.waiting_email)

    kb = ReplyKeyboardBuilder()
    kb.button(text="Пропустить")
    kb.button(text="Отмена")
    await message.answer("Введите ваш email или нажмите «Пропустить»:",
                         reply_markup=kb.as_markup(resize_keyboard=True))


@router.message(GuideForm.waiting_email)
async def guide_email(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await state.clear()
        return await message.answer("Отменено.", reply_markup=main_kb)

    email = None if message.text.lower() == "пропустить" else message.text.strip()

    data = await state.get_data()
    filename = data["filename"]
    name = data["name"]
    phone = data["phone"]
    await state.clear() 


    payload = LeadCreate(name=name, phone=phone, email=email, source="guide", note=filename)
    async with AsyncSessionLocal() as db:
        await create_lead(db, payload)


    path = os.path.join(STATIC_DIR, "guieds", filename)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        await message.answer_document(FSInputFile(path), reply_markup=main_kb)
    else:
        await message.answer("Гайд не найден или пустой, мы свяжемся с вами.", reply_markup=main_kb)


    for admin in ADMIN_CHAT_IDS:
        await message.bot.send_message(
            admin,
            f"Новый лид (гайд): {name} | {phone} | {email or '-'} | {filename}"
        )

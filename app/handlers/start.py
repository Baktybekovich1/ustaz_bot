from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from app.keyboards import main_kb

router = Router()

@router.message(Command(commands=["start", "help"]))
async def cmd_start(message: Message):
    await message.answer(
        "Привет 👋 Я бот курсов программирования. "
        "Хочешь узнать больше о наших курсах или получить бесплатный гайд?",
        reply_markup=main_kb
    )

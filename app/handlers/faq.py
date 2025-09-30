from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from app.keyboards import main_kb
router = Router()

FAQ = {
    "Какие курсы есть?": "Frontend, Backend, React.js, HTML/CSS",
    "Сколько стоит обучение?": "Цена по запросу. Оставьте контакт и мы отправим прайс.",
    "Можно ли совмещать с учёбой/работой?": "Да, большинство курсов гибкие по времени.",
    "Выдаёте ли сертификаты?": "Да, по окончанию курса выдаём сертификат.",
    "Смогу ли я устроиться на работу после курса?": "Курсы ориентированы на трудоустройство, но итог зависит от вашего прогресса.",
    "Вы лох?" : "Нет ты долбан",
}

@router.message(F.text.contains("Задать вопрос"))
async def on_faq(message: Message):
    kb = ReplyKeyboardBuilder()
    for q in FAQ.keys():
        kb.button(text=q)
    kb.button(text="⬅️ Назад")
    kb.adjust(1)
    await message.answer(
        "Частые вопросы, выберите один:",
        reply_markup=kb.as_markup(resize_keyboard=True)
    )

@router.message(F.text == "⬅️ Назад")
async def go_back(message: Message):
    kb = ReplyKeyboardBuilder()
    kb.button(text="Задать вопрос")
    kb.adjust(1)
    await message.answer(
        "Вы вернулись в главное меню.",
        reply_markup=main_kb)

@router.message(F.text.in_(FAQ.keys()))
async def get_answer(message: Message):
    await message.answer(FAQ[message.text])

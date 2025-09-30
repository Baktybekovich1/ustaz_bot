from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from app.keyboards import course_inline 

router = Router()

@router.message(lambda message: message.text and "Узнать о курсах" in message.text)
async def on_courses(message: Message):
    await message.answer("Выберите курс:", reply_markup=course_inline())

@router.callback_query(lambda c: c.data and c.data.startswith("course:"))
async def course_callback(query: CallbackQuery):
    course = query.data.split(":",1)[1]
    programs = {
        "Frontend": "HTML, CSS, JavaScript, React. Длительность 9 месяцев.",
        "Backend": "Python, Django/DRF, PostgreSQL. Длительность 9 месяцев.",
        "React.js": "React, hooks, routing, state management. 3 месяца.",
        "HTML/CSS": "HTML5, CSS3, адаптивная вёрстка. 3 месяца."
    }
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Записаться", callback_data=f"signup:{course}")]
        ]
    )

    await query.message.edit_text(
        f"{course}\n\n{programs.get(course,'Программа')}\n\nФормат: онлайн/офлайн\nЦена: по запросу",
        reply_markup=kb
    )
    await query.answer()

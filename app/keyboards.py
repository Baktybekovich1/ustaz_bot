from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📚 Узнать о курсах"), KeyboardButton(text="🎁 Получить бесплатный гайд")],
        [ KeyboardButton(text="❓ Задать вопрос")]
    ],
    resize_keyboard=True
)

def course_inline():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Frontend", callback_data="course:Frontend")],
            [InlineKeyboardButton(text="Backend", callback_data="course:Backend")],
            [InlineKeyboardButton(text="React.js", callback_data="course:React.js")],
            [InlineKeyboardButton(text="HTML/CSS", callback_data="course:HTML/CSS")]
        ]
    )

def guide_inline() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Гайд Frontend",
                    callback_data="guide:frontend_guide.pdf"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Гайд Backend",
                    callback_data="guide:backend_guide.pdf"
                )
            ]
        ]
    )
    return kb


cancel_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Отмена")]],
    resize_keyboard=True
)

format_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Онлайн"), KeyboardButton(text="Офлайн")],
        [KeyboardButton(text="❌ Отмена")]
    ],
    resize_keyboard=True
)
# app/handlers/admin.py
import io
import json
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types.input_file import InputFile
from app.db import AsyncSessionLocal
from app.models import Lead
from app.config import ADMIN_CHAT_IDS

router = Router()
MAX_RECORDS_PER_FILE = 1000


# @router.message(lambda m: m.text and m.text.lower() == "export")
@router.message(Command(commands=["export"]))
async def export_cmd(message: Message):
    await message.answer(f"Команда export получена от {message.from_user.id}")
    if message.from_user.id not in ADMIN_CHAT_IDS:
        return await message.answer("Доступ запрещён.")
    async with AsyncSessionLocal() as db:
        result = await db.execute(Lead.__table__.select())
        rows = result.all()

    await message.answer(rows)

    data_list = [dict(r._mapping) for r in rows]
    chunks = [
        data_list[i:i + MAX_RECORDS_PER_FILE]
        for i in range(0, len(data_list), MAX_RECORDS_PER_FILE)
    ]

    for idx, chunk in enumerate(chunks, start=1):
        buf = io.BytesIO(json.dumps(chunk, indent=2, default=str).encode("utf-8"))
        buf.seek(0)
        filename = f"leads_part{idx}.json" if len(chunks) > 1 else "leads.json"

        input_file = InputFile(file=buf, filename=filename)

        await message.answer_document(input_file)

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import asyncio
import logging
from dotenv import load_dotenv
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from rag.pipeline import RAGPipeline

load_dotenv()

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher()
rag = RAGPipeline()   # bir marta yuklanadi

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Salom! Men Soliq bo'yicha yordamchi Ai Assistantman.\n"
        "Har qanday soliq yo'nalishidagi savolingizni yozing \n (masalan: 'Yuridik shaxslar uchun yer solig'i stavkasi qancha?')"
    )

@dp.message()
async def handle_question(message: Message):
    await message.answer("🔍 Javob qidirilmoqda...")
    
    try:
        answer = await asyncio.to_thread(rag.query, message.text.strip())
        await message.answer(answer)
    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await message.answer("❌ Xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("🚀 Bot ishga tushdi...")
    asyncio.run(dp.start_polling(bot))
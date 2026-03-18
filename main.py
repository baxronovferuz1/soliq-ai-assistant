import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

import logging
import os
import asyncio

from fastapi import FastAPI, Request
import requests
from dotenv import load_dotenv

from rag.pipeline import RAGPipeline

load_dotenv()

# 🔹 Config
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

app = FastAPI()
rag = RAGPipeline()  # 🔥 1 marta yuklanadi (MUHIM)

logging.basicConfig(level=logging.INFO)


@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()

    try:
        message = data.get("message", {})
        text = message.get("text", "")
        chat_id = message.get("chat", {}).get("id")

        if not text or not chat_id:
            return {"ok": True}

        # 🔹 "typing..." effekt
        requests.post(f"{TELEGRAM_API}/sendChatAction", json={
            "chat_id": chat_id,
            "action": "typing"
        })

        # 🔹 AI chaqirish (blocking → threadga o‘tkazamiz)
        answer = await asyncio.to_thread(rag.query, text.strip())

        # 🔹 Javob yuborish
        requests.post(f"{TELEGRAM_API}/sendMessage", json={
            "chat_id": chat_id,
            "text": answer
        })

    except Exception as e:
        logging.error(f"Xatolik: {e}")

        if "chat_id" in locals():
            requests.post(f"{TELEGRAM_API}/sendMessage", json={
                "chat_id": chat_id,
                "text": "❌ Xatolik yuz berdi. Iltimos, keyinroq urinib ko‘ring."
            })

    return {"ok": True}

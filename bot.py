import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from utils import analyze_trade
from dotenv import load_dotenv
from PIL import Image
import pytesseract

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Пришли фото трейда, и я дам анализ AI.")

@dp.message()
async def handle_trade_photo(message: types.Message):
    if message.photo:
        photo = message.photo[-1]
        file = await bot.get_file(photo.file_id)
        path = f"downloads/{photo.file_id}.jpg"
        await photo.download(destination_file=path)

        # OCR для извлечения текста с фото (питомцы и валюты)
        text = pytesseract.image_to_string(Image.open(path))

        # В реальном проекте здесь нужно парсить текст в структуры my_items, their_items
        my_items = ["пример_питомца"]
        their_items = ["пример_питомца"]
        my_values = {"pet1": 50}
        their_values = {"pet2": 40}

        result = analyze_trade(my_items, their_items, my_values, their_values)
        await message.answer(result)
    else:
        await message.answer("Пожалуйста, пришли фото трейда.")

if __name__ == "__main__":
    import asyncio
    from aiogram import F
    asyncio.run(dp.start_polling(bot))

# bot.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from utils.api import get_pet_values
from utils.ocr import extract_trade_text
from utils.ai_analysis import analyze_trade

import os
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Создаем бот и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()  # В 3.x Bot НЕ передается сюда

# Пример простого хэндлера /start
@dp.message(Command(commands=["start"]))
async def start_handler(message: Message):
    await message.answer("Привет! Я бот.")

# Пример хэндлера, использующего твои utils
@dp.message(Command(commands=["trade"]))
async def trade_handler(message: Message):
    # Берем данные через твой модуль api
    pet_values = get_pet_values()
    
    # Анализируем через AI
    analysis_result = analyze_trade(pet_values)
    
    await message.answer(f"Результат анализа: {analysis_result}")

# Пример хэндлера для OCR (если нужно)
@dp.message(Command(commands=["ocr"]))
async def ocr_handler(message: Message):
    # Берем текст через OCR из картинки (ссылка или файл)
    text = extract_trade_text("sample_image.png")  # тут путь к картинке
    await message.answer(f"Распознанный текст: {text}")

# Запуск бота
if __name__ == "__main__":
    dp.run_polling(bot)  # В 3.x бот передается сюда

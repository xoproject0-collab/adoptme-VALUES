import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from utils.api import get_pet_values
from utils.ocr import extract_trade_text
from utils.ai_analysis import analyze_trade
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher()

# глобальные переменные для цен
pet_values = {}

async def update_values_loop():
    global pet_values
    while True:
        pet_values = get_pet_values()
        await asyncio.sleep(600)  # обновляем каждые 10 минут

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_trade_photo(message: types.Message):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    path = f"temp_{photo.file_id}.jpg"
    await file.download(destination_file=path)

    trade_text = extract_trade_text(path)
    # пример простой обработки: разбиваем на строки и ищем имена питомцев
    lines = [l.strip() for l in trade_text.splitlines() if l.strip()]
    my_items = lines[0].split(",")  # грубая имитация
    their_items = lines[1].split(",")

    advice = analyze_trade(my_items, their_items, pet_values, pet_values)
    await message.reply(advice)

async def main():
    asyncio.create_task(update_values_loop())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

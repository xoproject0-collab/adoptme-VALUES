import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from utils.api import get_pet_values
from utils.ocr import extract_trade_text
from utils.ai_analysis import analyze_trade
from dotenv import load_dotenv

load_dotenv()

# Создаём бот и диспетчер (v2.25.2)
bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))


# глобальные переменные для цен
pet_values = {}

async def update_values_loop():
    global pet_values
    while True:
        pet_values = get_pet_values()
        await asyncio.sleep(600)  # обновляем каждые 10 минут

# Обработка фото трейдов
@dp.message_handler(content_types=['photo'])
async def handle_trade_photo(message: types.Message):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    path = f"temp_{photo.file_id}.jpg"
    await file.download(destination_file=path)

    trade_text = extract_trade_text(path)
    lines = [l.strip() for l in trade_text.splitlines() if l.strip()]
    
    if len(lines) >= 2:
        my_items = lines[0].split(",")
        their_items = lines[1].split(",")
    else:
        await message.reply("Не удалось распознать трейд. Попробуй другой скриншот.")
        return

    advice = analyze_trade(my_items, their_items, pet_values, pet_values)
    await message.reply(advice)

async def main():
    asyncio.create_task(update_values_loop())
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())

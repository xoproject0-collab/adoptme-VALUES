import os
import time
import threading
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.utils import executor
from dotenv import load_dotenv
from pets_values import update_values, get_pet_value
from utils import ocr_image, analyze_trade

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Автообновление цен каждые 10 минут
def auto_update():
    while True:
        update_values()
        time.sleep(600)

threading.Thread(target=auto_update, daemon=True).start()

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Привет! Пришли мне скрин трейда, и я скажу, выгодно ли соглашаться.")

@dp.message_handler(content_types=ContentType.PHOTO)
async def photo_trade(message: types.Message):
    # Сохраняем фото
    photo = message.photo[-1]
    file_path = f"{photo.file_id}.jpg"
    await photo.download(file_path)
    
    # Распознаем текст
    text = ocr_image(file_path)
    
    if not text.strip():
        await message.reply("Не смог распознать текст на фото.")
        return
    
    # Анализ AI
    analysis = analyze_trade(text)
    await message.reply(analysis)

@dp.message_handler(content_types=ContentType.TEXT)
async def text_trade(message: types.Message):
    # Анализ текста прямо через AI
    analysis = analyze_trade(message.text)
    await message.reply(analysis)

if __name__ == "__main__":
    update_values()  # первое обновление при старте
    executor.start_polling(dp, skip_updates=True)
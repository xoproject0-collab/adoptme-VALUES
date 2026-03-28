from PIL import Image
import pytesseract
from pets_values import get_pet_value
import openai
import os

openai.api_key = os.getenv("OPENAI_KEY")

# Распознаем текст с картинки
def ocr_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

# Анализ трейда через AI
def analyze_trade(text):
    """
    text - распознанный текст с фото, формат:
    'Я даю: dog, cat\nОн даёт: dragon, unicorn'
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role": "system",
                "content": "Ты эксперт в игре Adopt Me, оценивай выгодность трейдов, учитывай цены питомцев и их ликвидность."
            },{
                "role": "user",
                "content": text
            }],
            temperature=0.3
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Ошибка анализа трейда: {e}"
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_trade(my_items, their_items, my_values, their_values):
    """
    my_items: список ваших предметов
    their_items: список предметов другого игрока
    my_values: словарь с валютами ваших питомцев
    their_values: словарь с валютами их питомцев
    """

    prompt = f"""
Я эксперт по трейдам Adopt Me.
Я анализирую трейд:
Я отдаю: {my_items} с валютами {my_values}
Мне дают: {their_items} с валютами {their_values}

Скажи:
1. Стоит ли соглашаться?
2. Обоснуй решение подробно.
3. Укажи плюсы и минусы трейда.
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )

    return response.choices[0].message.content

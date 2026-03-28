import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_trade(my_items, their_items, my_values, their_values):
    """
    AI анализирует трейд и аргументирует
    """
    prompt = f"""
Ты эксперт по AdoptMe. Мой трейд: 
Я отдаю: {my_items} (ценность {sum([my_values.get(i,0) for i in my_items])})
Мне дают: {their_items} (ценность {sum([their_values.get(i,0) for i in their_items])})

Скажи: соглашаться или нет и почему, объясни как человеку.
"""
    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}],
        temperature=0.7
    )
    return resp.choices[0].message.content

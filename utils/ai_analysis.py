import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_trade(my_items, their_items, my_values, their_values):
    # подсчет разницы value
    my_sum = sum(my_values.get(i.strip(), 0) for i in my_items)
    their_sum = sum(their_values.get(i.strip(), 0) for i in their_items)

    prompt = f"""
    Я эксперт по трейдам.
    Я даю анализ: Мои предметы {my_items} (value={my_sum})
    Их предметы {their_items} (value={their_sum})
    Посоветуй: соглашаться или нет и аргументируй простыми словами.
    """

    try:
        resp = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        return resp.choices[0].text.strip()
    except Exception as e:
        return f"Ошибка ИИ: {e}"

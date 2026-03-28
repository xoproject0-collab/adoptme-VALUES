import requests

API_URL = "https://adoptmevalues.gg/api/v1/values?sortBy=position&limit=100&page=1"

pet_values = {}

def update_values():
    global pet_values
    try:
        r = requests.get(API_URL)
        r.raise_for_status()
        data = r.json()
        pet_values = {item['name'].lower(): item['value'] for item in data['data']}
        print("Цены питомцев обновлены")
    except Exception as e:
        print("Ошибка при обновлении цен:", e)

def get_pet_value(name):
    return pet_values.get(name.lower(), 0)
import requests
import os

API_BASE = os.getenv("API_BASE_URL")

def get_pet_values():
    """Берёт цены питомцев через API"""
    url = f"{API_BASE}/values?sortBy=position&limit=100&page=1"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        return {item['name']: item['value'] for item in data['data']}
    return {}

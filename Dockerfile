# Используем стабильный Python 3.12
FROM python:3.12-slim

WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Переменная окружения для Telegram
ENV TELEGRAM_TOKEN=${TELEGRAM_TOKEN}

# Запуск бота
CMD ["python", "bot.py"]

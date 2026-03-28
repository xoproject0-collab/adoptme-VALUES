FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential libjpeg-dev zlib1g-dev \
    libtiff-dev libfreetype6-dev liblcms2-dev \
    libwebp-dev tcl8.6-dev tk8.6-dev python3-tk \
    libharfbuzz-dev libfribidi-dev libxcb1-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "bot.py"]

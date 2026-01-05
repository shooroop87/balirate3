FROM python:3.11-slim

# Установка системных зависимостей (добавлен gettext для compilemessages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    libcairo2-dev \
    libffi-dev \
    gettext \
  && rm -rf /var/lib/apt/lists/*

# Создание пользователя для безопасности
RUN useradd --create-home --shell /bin/bash app

WORKDIR /app

# Копирование requirements и установка зависимостей
COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Очистка старых статических файлов
RUN rm -rf /app/collected_static/* || true

# Сборка статических файлов
RUN python manage.py collectstatic --noinput --clear --verbosity=2

# Timestamp для отслеживания версии
RUN echo "BUILD_TIMESTAMP=$(date +%Y%m%d_%H%M%S)" > /app/.build_info && \
    echo "BUILD_HASH=$(echo $RANDOM | md5sum | head -c 8)" >> /app/.build_info

# Изменение владельца файлов
RUN chown -R app:app /app

USER app

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
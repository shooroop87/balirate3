# balirate — Django

## 🚀 Запуск проекта локально через Docker

### 1. Клонируй репозиторий

```bash
git clone https://github.com/your/repo.git
cd your-repo
```

### 2. Собери и запусти

```bash
docker-compose up --build
```

### 3. Открой сайт

Перейди в браузере: [http://localhost:8000](http://localhost:8000)

---

## 🌍 Мультиязычность

Для обновления переводов:

```bash
docker-compose run web django-admin makemessages -l ru
docker-compose run web django-admin compilemessages
```

Все переводы в `core/locale/`

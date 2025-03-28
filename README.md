
# Telegram Bot для Звітів

Телеграм бот для автоматизації створення звітів про виконані роботи інженерами.

## Структура проєкту

- `bot/` - Основні файли бота
  - `__init__.py` - Ініціалізація модуля
  - `handlers.py` - Обробники команд і повідомлень
  - `keyboards.py` - Клавіатури для бота
  - `states.py` - Стани для FSM (Finite State Machine)
- `utils/` - Утиліти та допоміжні функції
  - `__init__.py` - Ініціалізація модуля
  - `background.py` - Фонові процеси (Flask сервер для підтримки бота)
- `data/` - Дані та ресурси
  - `__init__.py` - Ініціалізація модуля
- `main.py` - Головний файл для запуску бота

## Встановлення та запуск

1. Встановіть залежності: `pip install -r requirements.txt`
2. Створіть файл `.env` з токеном бота (використовуйте `.env.example` як шаблон)
3. Запустіть бота: `python main.py`

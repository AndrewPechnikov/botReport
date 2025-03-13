
from aiogram.fsm.state import State, StatesGroup

class Report(StatesGroup):
    """
    Клас для управління станами при створенні звіту
    """
    stNumber = State()  # Номер станції
    description = State()  # Опис проблеми
    solution = State()  # Рішення
    work_done = State()  # Виконані роботи
    distance = State()  # Відстань
    photos = State()  # Фото

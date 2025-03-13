
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
    photos = State()  # Фотографії

class Equipment(StatesGroup):
    """
    Клас для управління станами при роботі з обладнанням
    """
    action = State()  # Дія (додати, призначити, показати)
    name = State()  # Назва обладнання
    quantity = State()  # Кількість
    engineer = State()  # Інженер

class Salary(StatesGroup):
    """
    Клас для управління станами при розрахунку зарплати
    """
    engineer = State()  # Інженер
    month = State()  # Місяцьонані роботи
    distance = State()  # Відстань
    photos = State()  # Фото

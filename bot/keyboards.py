
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Головна клавіатура з кнопками основних функцій
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Згенерувати звіт')],
    [KeyboardButton(text='Відправити звіт в бота')],
    [KeyboardButton(text='Відправити звіт в service point')]
], resize_keyboard=True, input_field_placeholder='Оберіть пункт меню...')

# Розширена головна клавіатура
kb_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Згенерувати звіт')],
        [KeyboardButton(text='Обладнання')],
        [KeyboardButton(text='Розрахунок зарплати')]
    ],
    resize_keyboard=True)

# Клавіатура для пропуску кроку
kb_skip = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Пропустити")]],
    resize_keyboard=True)

# Клавіатура для роботи з обладнанням
kb_equipment = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Додати обладнання')],
        [KeyboardButton(text='Призначити обладнання')],
        [KeyboardButton(text='Показати список обладнання')],
        [KeyboardButton(text='Назад')]
    ],
    resize_keyboard=True)

# Клавіатура для місяців
kb_months = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Січень'), KeyboardButton(text='Лютий'), KeyboardButton(text='Березень')],
        [KeyboardButton(text='Квітень'), KeyboardButton(text='Травень'), KeyboardButton(text='Червень')],
        [KeyboardButton(text='Липень'), KeyboardButton(text='Серпень'), KeyboardButton(text='Вересень')],
        [KeyboardButton(text='Жовтень'), KeyboardButton(text='Листопад'), KeyboardButton(text='Грудень')],
        [KeyboardButton(text='За весь час')]
    ],
    resize_keyboard=True)

# Список станцій для швидкого вибору
stationList = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Станція 1")], 
    [KeyboardButton(text="Станція 2")],
    [KeyboardButton(text="Станція 3")]
], resize_keyboard=True)

# Додаткова клавіатура (якщо потрібна)
additional_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='1')],
    [KeyboardButton(text='2')]
], resize_keyboard=True)

# Навігаційна клавіатура
navigation = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Назад')],
    [KeyboardButton(text='Завершити')]
], resize_keyboard=True)

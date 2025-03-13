
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Головна клавіатура з кнопками основних функцій
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Згенерувати звіт')],
    [KeyboardButton(text='Відправити звіт в бота')],
    [KeyboardButton(text='Відправити звіт в service point')]
], resize_keyboard=True, input_field_placeholder='Оберіть пункт меню...')

# Спрощена головна клавіатура (використовується зараз)
kb_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Згенерувати звіт')],
        # [KeyboardButton(text='Відправити звіт')]
    ],
    resize_keyboard=True)

# Клавіатура для пропуску кроку
kb_skip = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Пропустити")]],
    resize_keyboard=True)

# Список станцій для швидкого вибору
stationList = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='1')],
    [KeyboardButton(text='2')]
], resize_keyboard=True)

# Навігаційна клавіатура
navigation = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Назад')],
    [KeyboardButton(text='Завершити')]
], resize_keyboard=True)

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Згенерувати звіт')],
    [KeyboardButton(text='Відправити звіт в бота')],
    [KeyboardButton(text='Відправити звіт в service point')]
], resize_keyboard=True, input_field_placeholder='Оберіть пункт меню...')

stationList = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='1')],
    [KeyboardButton(text='2')]
], resize_keyboard=True)

navigation = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Назад')],
    [KeyboardButton(text='Завершити')]
], resize_keyboard=True)

skip_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Пропустити')]
], resize_keyboard=True)
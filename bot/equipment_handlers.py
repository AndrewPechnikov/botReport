
from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import datetime

from bot.states import Equipment, Salary
from bot.keyboards import kb_main, kb_equipment, kb_months
from utils.excel_manager import ExcelManager

# Створюємо роутер для обробки повідомлень
equipment_router = Router()
excel_manager = ExcelManager()

# Обробник команди /equipment
@equipment_router.message(F.text == "Обладнання")
async def equipment_menu(message: Message):
    """
    Показує меню роботи з обладнанням
    """
    await message.answer("Меню роботи з обладнанням:", reply_markup=kb_equipment)

# Обробник для повернення в головне меню
@equipment_router.message(F.text == "Назад")
async def back_to_main(message: Message, state: FSMContext):
    """
    Повертає користувача в головне меню
    """
    await state.clear()
    await message.answer("Головне меню:", reply_markup=kb_main)

# Обробник для додавання обладнання
@equipment_router.message(F.text == "Додати обладнання")
async def add_equipment_start(message: Message, state: FSMContext):
    """
    Початок процесу додавання обладнання
    """
    await state.set_state(Equipment.name)
    await message.answer("Введіть назву обладнання:")

@equipment_router.message(Equipment.name)
async def add_equipment_name(message: Message, state: FSMContext):
    """
    Збереження назви обладнання і запит кількості
    """
    await state.update_data(name=message.text)
    await state.set_state(Equipment.quantity)
    await message.answer("Введіть кількість:")

@equipment_router.message(Equipment.quantity)
async def add_equipment_quantity(message: Message, state: FSMContext):
    """
    Збереження кількості і запит інженера
    """
    try:
        quantity = int(message.text)
        await state.update_data(quantity=quantity)
        await state.set_state(Equipment.engineer)
        await message.answer("Введіть ім'я інженера (або пропустіть):", 
                             reply_markup=ReplyKeyboardMarkup(
                                 keyboard=[[KeyboardButton(text="Пропустити")]],
                                 resize_keyboard=True))
    except ValueError:
        await message.answer("Будь ласка, введіть числове значення для кількості.")

@equipment_router.message(Equipment.engineer, F.text == "Пропустити")
async def skip_engineer(message: Message, state: FSMContext):
    """
    Обробка пропуску інженера
    """
    data = await state.get_data()
    success, message_text = excel_manager.add_equipment(
        data.get("name"), 
        data.get("quantity"),
        None
    )
    
    await state.clear()
    await message.answer(message_text, reply_markup=kb_equipment)

@equipment_router.message(Equipment.engineer)
async def add_equipment_engineer(message: Message, state: FSMContext):
    """
    Збереження інженера і додавання обладнання
    """
    data = await state.get_data()
    success, message_text = excel_manager.add_equipment(
        data.get("name"), 
        data.get("quantity"),
        message.text
    )
    
    await state.clear()
    await message.answer(message_text, reply_markup=kb_equipment)

# Обробник для призначення обладнання
@equipment_router.message(F.text == "Призначити обладнання")
async def assign_equipment_start(message: Message, state: FSMContext):
    """
    Початок процесу призначення обладнання
    """
    df = excel_manager.get_equipment_list()
    if df.empty:
        await message.answer("Список обладнання порожній.", reply_markup=kb_equipment)
        return
    
    await state.set_state(Equipment.name)
    
    # Створюємо клавіатуру з наявного обладнання
    equipment_buttons = []
    for name in df['Назва'].unique():
        equipment_buttons.append([KeyboardButton(text=name)])
    
    equipment_keyboard = ReplyKeyboardMarkup(
        keyboard=equipment_buttons + [[KeyboardButton(text="Скасувати")]],
        resize_keyboard=True
    )
    
    await message.answer("Виберіть обладнання для призначення:", reply_markup=equipment_keyboard)

@equipment_router.message(Equipment.name, F.text == "Скасувати")
async def cancel_assign(message: Message, state: FSMContext):
    """
    Скасування призначення обладнання
    """
    await state.clear()
    await message.answer("Операцію скасовано.", reply_markup=kb_equipment)

@equipment_router.message(Equipment.name)
async def assign_equipment_name(message: Message, state: FSMContext):
    """
    Збереження назви обладнання для призначення і запит інженера
    """
    df = excel_manager.get_equipment_list()
    if message.text not in df['Назва'].values:
        await message.answer("Такого обладнання немає в списку. Спробуйте ще раз.")
        return
    
    await state.update_data(name=message.text)
    await state.set_state(Equipment.engineer)
    await message.answer("Введіть ім'я інженера, якому призначається обладнання:")

@equipment_router.message(Equipment.engineer)
async def assign_equipment_engineer(message: Message, state: FSMContext):
    """
    Збереження інженера і призначення обладнання
    """
    data = await state.get_data()
    success, message_text = excel_manager.assign_equipment(
        data.get("name"),
        message.text
    )
    
    await state.clear()
    await message.answer(message_text, reply_markup=kb_equipment)

# Обробник для показу списку обладнання
@equipment_router.message(F.text == "Показати список обладнання")
async def show_equipment_list(message: Message):
    """
    Відображення списку обладнання
    """
    df = excel_manager.get_equipment_list()
    if df.empty:
        await message.answer("Список обладнання порожній.", reply_markup=kb_equipment)
        return
    
    equipment_text = "📋 Список обладнання:\n\n"
    for _, row in df.iterrows():
        engineer = row.get('Інженер', 'Не призначено')
        if pd.isna(engineer):
            engineer = 'Не призначено'
        
        equipment_text += f"📦 {row['Назва']} - {row['Кількість']} шт.\n   👨‍🔧 Інженер: {engineer}\n\n"
    
    await message.answer(equipment_text, reply_markup=kb_equipment)

# Обробники для розрахунку зарплати
@equipment_router.message(F.text == "Розрахунок зарплати")
async def salary_calculation_start(message: Message, state: FSMContext):
    """
    Початок процесу розрахунку зарплати
    """
    await state.set_state(Salary.engineer)
    await message.answer("Введіть ім'я інженера для розрахунку зарплати:")

@equipment_router.message(Salary.engineer)
async def salary_engineer(message: Message, state: FSMContext):
    """
    Збереження інженера і запит місяця
    """
    await state.update_data(engineer=message.text)
    await state.set_state(Salary.month)
    await message.answer("Виберіть місяць для розрахунку:", reply_markup=kb_months)

@equipment_router.message(Salary.month)
async def salary_month(message: Message, state: FSMContext):
    """
    Розрахунок і відображення зарплати
    """
    month_mapping = {
        'Січень': 1, 'Лютий': 2, 'Березень': 3,
        'Квітень': 4, 'Травень': 5, 'Червень': 6,
        'Липень': 7, 'Серпень': 8, 'Вересень': 9,
        'Жовтень': 10, 'Листопад': 11, 'Грудень': 12,
        'За весь час': None
    }
    
    month = month_mapping.get(message.text)
    data = await state.get_data()
    engineer = data.get("engineer")
    
    # Отримуємо звіти і розраховуємо зарплату
    total_amount = excel_manager.calculate_salary(engineer, month)
    
    month_text = message.text if message.text != 'За весь час' else 'весь час'
    
    await message.answer(
        f"💰 Зарплата інженера {engineer} за {month_text}:\n\n"
        f"Загальна сума: {total_amount} грн",
        reply_markup=kb_main
    )
    
    await state.clear()


from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.excel_manager import ExcelManager
import datetime

report_router = Router()
excel_manager = ExcelManager()

@report_router.message(F.text == "Зберегти звіт в базу")
async def save_report_to_excel(message: Message, state: FSMContext):
    """
    Обробник для збереження звіту в Excel
    """
    data = await state.get_data()
    
    # Отримуємо необхідні дані зі стану
    engineer = message.from_user.full_name
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    station = data.get("stNumber", "")
    works = data.get("work_done", [])
    distance = int(data.get("distance", 0))
    
    # Розраховуємо загальну суму
    total_amount = 0
    
    # Додаємо вартість виїзду
    travel_cost = distance * 8  # 8 грн за км
    total_amount += travel_cost
    
    # Додаємо вартість робіт
    for work in works:
        # Витягуємо суму з тексту роботи (формат: "Робота - XXX грн")
        try:
            price_str = work.split('-')[-1].strip()
            price = int(price_str.split()[0])
            total_amount += price
        except (ValueError, IndexError):
            continue
    
    # Зберігаємо звіт
    success, message_text = excel_manager.save_report(
        engineer, date, station, works, distance, total_amount
    )
    
    if success:
        await message.answer(f"Звіт успішно збережений в базу даних!\nЗагальна сума: {total_amount} грн")
    else:
        await message.answer(f"Помилка при збереженні звіту: {message_text}")

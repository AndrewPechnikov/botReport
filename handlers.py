from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InputMediaPhoto, InputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import pandas as pd

# Завантажуємо прайс із файлу
file_path = "НОВИЙ прайс для ІНЖЕНЕРІВ 06.2024.xlsx"
df = pd.read_excel(file_path, sheet_name="Лист1")

# Створюємо список варіантів робіт
job_list = [f"{row['Найменування роботи']} - {row['кошторис для інженера']} грн" for _, row in df.iterrows()]
job_list_for_button = [f"{row['Найменування роботи']} - {row['кошторис для інженера']} грн" for _, row in df.iterrows()]
router = Router()

class Report(StatesGroup):
    stNumber = State()  # Номер станції
    description = State()  # Опис проблеми
    solution = State()  # Рішення
    work_done = State()  # Виконані роботи
    distance = State()  # Відстань
    photos = State()  # Фото

# Клавіатури
kb_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Згенерувати звіт')],
        [KeyboardButton(text='Відправити звіт')]
    ],
    resize_keyboard=True
)

kb_skip = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Пропустити")]],
    resize_keyboard=True
)

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привіт! Це бот для створення звітів.', reply_markup=kb_main)

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Цей бот допомагає створювати звіти про виконану роботу.')

@router.message(F.text == 'Згенерувати звіт')
async def report(message: Message, state: FSMContext):
    await state.set_state(Report.stNumber)
    await message.answer('Оберіть номер станції:')

@router.message(Report.stNumber)
async def report_stNumber(message: Message, state: FSMContext):
    await state.update_data(stNumber=message.text)
    await state.set_state(Report.description)
    await message.answer("Опишіть проблему на станції:")

@router.message(Report.description)
async def report_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Report.solution)
    await message.answer("Як ви вирішили проблему?")

@router.message(Report.solution)
async def report_solution(message: Message, state: FSMContext):
    await state.update_data(solution=message.text)
    await state.set_state(Report.work_done)

    # Формуємо кнопки для вибору робіт у два ряди
    job_buttons = [[KeyboardButton(text="Готово")]]  # Додаємо кнопку "Готово" першою
    job_buttons += [[KeyboardButton(text=job_list[i]), KeyboardButton(text=job_list[i + 1])]
                    for i in range(0, min(len(job_list), 64) - 1, 2)]  # Додаємо кнопки в два ряди
    jobs_keyboard = ReplyKeyboardMarkup(keyboard=job_buttons)

    await message.answer("Оберіть виконані роботи (можна кілька, відправляйте повідомлення по черзі):", reply_markup=jobs_keyboard)

@router.message(Report.work_done)
async def report_work_done(message: Message, state: FSMContext):
    if message.text.lower() == "готово":
        await state.set_state(Report.distance)
        await message.answer("Скільки кілометрів ви проїхали для цієї роботи?")
        return

    data = await state.get_data()
    work_done = data.get("work_done", [])
    work_done.append(message.text)

    await state.update_data(work_done=work_done)
    await message.answer("Якщо більше робіт немає – напишіть 'Готово'. Якщо є ще, виберіть наступну.")

@router.message(F.text == 'Готово')
async def report_done(message: Message, state: FSMContext):
    await state.set_state(Report.distance)
    await message.answer("Скільки кілометрів ви проїхали для цієї роботи?")

@router.message(Report.distance)
async def report_distance(message: Message, state: FSMContext):
    await state.update_data(distance=message.text)
    await state.set_state(Report.photos)
    await message.answer("Додайте фото або натисніть 'Пропустити'.", reply_markup=kb_skip)

@router.message(Report.photos, F.photo)
async def report_photos(message: Message, state: FSMContext):
    data = await state.get_data()
    photos = data.get("photos", [])

    # Додаємо нове фото в список
    photos.append(message.photo[-1].file_id)  # Беремо найкращу якість фото

    await state.update_data(photos=photos)
    await message.answer("Фото збережено. Додайте ще або натисніть 'Пропустити'.", reply_markup=kb_skip)

@router.message(F.text == "Пропустити")
async def report_skip_photos(message: Message, state: FSMContext):
    data = await state.get_data()

    # Отримуємо список виконаних робіт і додаємо вартість виїзду
    work_done = data.get("work_done", [])
    distance = int(data.get("distance", 0))  # Отримуємо кілометраж
    travel_cost = distance * 8  # Розраховуємо вартість виїзду
    work_done.append(f"🚗 Виїзд на {distance} км - {travel_cost} грн")  # Додаємо у список робіт

    # Формуємо перше повідомлення (без робіт, але з фото)
    report_text_1 = (
        f"📍 **Номер станції:** {data.get('stNumber', 'Не вказано')}\n"
        f"📝 **Опис проблеми:** {data.get('description', 'Не вказано')}\n"
        f"✅ **Рішення:** {data.get('solution', 'Не вказано')}\n"
    )

    # Формуємо друге повідомлення (зі списком робіт, але без фото)
    work_done_text = "\n".join([f"   - **{job}**" for job in work_done])  # Форматування робіт
    report_text_2 = (
        f"📍 **Номер станції:** {data.get('stNumber', 'Не вказано')}\n"
        f"📝 **Опис проблеми:** {data.get('description', 'Не вказано')}\n"
        f"✅ **Рішення:** {data.get('solution', 'Не вказано')}\n"
        f"🔧 **Виконані роботи:**\n$\n{work_done_text}\n$\n"
    )

    # Перевіряємо, чи є фото
    if "photos" in data and data["photos"]:
        # Створюємо список InputMediaPhoto для кожного фото
        media = [InputMediaPhoto(media=photo) for photo in data["photos"]]

        # Відправляємо всі фото разом з першим звітом
        await message.answer_media_group(media=media)  # Відправляємо фото в групі
        await message.answer(report_text_1, parse_mode="Markdown")  # Відправляємо текст звіту
    else:
        await message.answer(report_text_1, parse_mode="Markdown")  # Якщо фото немає, просто текст

    # Відправляємо друге повідомлення з роботами
    await message.answer(report_text_2, parse_mode="Markdown")

    await message.answer("Звіт збережено. Ви можете надіслати його в бот або в service point.", reply_markup=kb_main)
    await state.clear()

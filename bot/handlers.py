from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InputMediaPhoto, InputFile, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
import pandas as pd

# Імпортуємо стани з окремого файлу
from bot.states import Report
# Імпортуємо клавіатури з окремого файлу
from bot.keyboards import kb_main, kb_skip

# Створюємо роутер для обробки повідомлень
router = Router()

# Завантажуємо прайс із файлу
file_path = "data/НОВИЙ прайс для ІНЖЕНЕРІВ 06.2024.xlsx"
try:
    df = pd.read_excel(file_path, sheet_name="Лист1")

    # Створюємо список варіантів робіт
    job_list = [
        f"{row['Найменування роботи']} - {row['кошторис для інженера']} грн"
        for _, row in df.iterrows()
    ]
    job_list_for_button = [
        f"{row['Найменування роботи']} - {row['кошторис для інженера']} грн"
        for _, row in df.iterrows()
    ]
except Exception as e:
    print(f"Помилка при завантаженні прайсу: {e}")
    job_list = []
    job_list_for_button = []


@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    Обробник команди /start
    Виводить привітання та показує головну клавіатуру
    """
    await message.answer('Привіт! Це бот для створення звітів.',
                         reply_markup=kb_main)


@router.message(Command('help'))
async def cmd_help(message: Message):
    """
    Обробник команди /help
    Виводить довідкову інформацію про бота
    """
    await message.answer(
        'Цей бот допомагає створювати звіти про виконану роботу.')


@router.message(F.text == 'Згенерувати звіт')
async def report(message: Message, state: FSMContext):
    """
    Обробник кнопки "Згенерувати звіт"
    Запускає послідовність створення звіту, встановлюючи перший стан
    """
    await message.answer("Впишіть номер станції:",
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(Report.stNumber)


@router.message(Report.stNumber)
async def report_stNumber(message: Message, state: FSMContext):
    """
    Обробник для стану введення номера станції
    Зберігає номер станції та переходить до наступного стану
    """
    await state.update_data(stNumber=message.text)
    await state.set_state(Report.description)
    await message.answer("Опишіть проблему на станції:")


@router.message(Report.description)
async def report_description(message: Message, state: FSMContext):
    """
    Обробник для стану опису проблеми
    Зберігає опис проблеми та переходить до наступного стану
    """
    await state.update_data(description=message.text)
    await state.set_state(Report.solution)
    await message.answer("Як ви вирішили проблему?")


@router.message(Report.solution)
async def report_solution(message: Message, state: FSMContext):
    """
    Обробник для стану рішення проблеми
    Зберігає рішення та переходить до вибору виконаних робіт
    """
    await state.update_data(solution=message.text)
    await state.set_state(Report.work_done)

    # Формуємо кнопки для вибору робіт у два ряди
    job_buttons = [[KeyboardButton(text="Готово")]
                   ]  # Додаємо кнопку "Готово" першою
    job_buttons += [[
        KeyboardButton(text=job_list[i]),
        KeyboardButton(text=job_list[i + 1])
    ] for i in range(0,
                     min(len(job_list), 64) - 1, 2)
                    ]  # Додаємо кнопки в два ряди
    jobs_keyboard = ReplyKeyboardMarkup(keyboard=job_buttons)

    await message.answer(
        "Оберіть виконані роботи (можна кілька, відправляйте повідомлення по черзі):",
        reply_markup=jobs_keyboard)


@router.message(Report.work_done)
async def report_work_done(message: Message, state: FSMContext):
    """
    Обробник для стану вибору виконаних робіт
    Зберігає обрані роботи або переходить далі, якщо отримано "Готово"
    """
    if message.text.lower() == "готово":
        await state.set_state(Report.distance)
        await message.answer("Скільки кілометрів ви проїхали для цієї роботи?")
        return

    data = await state.get_data()
    work_done = data.get("work_done", [])
    work_done.append(message.text)

    await state.update_data(work_done=work_done)
    await message.answer(
        "Якщо більше робіт немає – напишіть 'Готово'. Якщо є ще, виберіть наступну."
    )


@router.message(F.text == 'Готово')
async def report_done(message: Message, state: FSMContext):
    """
    Обробник для кнопки "Готово" при виборі робіт
    Переходить до вводу відстані
    """
    await state.set_state(Report.distance)
    await message.answer("Скільки кілометрів ви проїхали для цієї роботи?")


@router.message(Report.distance)
async def report_distance(message: Message, state: FSMContext):
    """
    Обробник для стану введення відстані
    Зберігає відстань та переходить до завантаження фото
    """
    await state.update_data(distance=message.text)
    await state.set_state(Report.photos)
    await message.answer("Додайте фото або натисніть 'Пропустити'.",
                         reply_markup=kb_skip)


@router.message(Report.photos, F.photo)
async def report_photos(message: Message, state: FSMContext):
    """
    Обробник для стану завантаження фото
    Зберігає отримані фото
    """
    data = await state.get_data()
    photos = data.get("photos", [])

    # Додаємо нове фото в список
    photos.append(message.photo[-1].file_id)  # Беремо найкращу якість фото

    await state.update_data(photos=photos)
    await message.answer(
        "Фото збережено. Додайте ще або натисніть 'Пропустити'.",
        reply_markup=kb_skip)


@router.message(F.text == "Пропустити")
async def report_skip_photos(message: Message, state: FSMContext):
    """
    Обробник для кнопки "Пропустити" при завантаженні фото
    Формує та відправляє готовий звіт
    """
    data = await state.get_data()
    work_done = data.get("work_done", [])
    distance = int(data.get("distance", 0))
    travel_cost = distance * 8
    total_amount = travel_cost

    report_text = f"📋 *Звіт про виконану роботу*\n\n"
    report_text += f"🔢 *Станція:* {data.get('stNumber')}\n\n"
    report_text += f"❓ *Проблема:* {data.get('description')}\n\n"
    report_text += f"✅ *Рішення:* {data.get('solution')}\n\n"
    report_text += "📝 *Виконані роботи:*\n"

    for work in work_done:
        report_text += f"- {work}\n"
        for _, row in df.iterrows():
            if row["Найменування роботи"] in work:
                total_amount += row["кошторис для інженера"]
                break

    report_text += f"\n💰 *Загальна сума:* {total_amount} грн"

    # Додаємо клавіатуру для збереження в базу
    save_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Зберегти звіт в базу")],
                  [KeyboardButton(text="Згенерувати звіт")]],
        resize_keyboard=True)

    # Очищуємо стан
    await state.clear()

    # Відправляємо звіт
    await message.answer(report_text,
                         parse_mode="Markdown",
                         reply_markup=save_keyboard)

    # Якщо є фотографії, відправляємо їх
    photos = data.get("photos", [])
    if photos:
        media_group = []
        for photo_id in photos:
            media_group.append(InputMediaPhoto(media=photo_id))
        await message.answer_media_group(media=media_group)

    # Формуємо перше повідомлення (без робіт, але з фото)
    report_text_1 = (
        f"📍 **Номер станції:** {data.get('stNumber', 'Не вказано')}\n"
        f"📝 **Опис проблеми:** {data.get('description', 'Не вказано')}\n"
        f"✅ **Рішення:** {data.get('solution', 'Не вказано')}\n")

    # Формуємо друге повідомлення (зі списком робіт, але без фото)
    work_done_text = "\n".join([f"   - **{job}**"
                                for job in work_done])  # Форматування робіт
    report_text_2 = (
        f"📍 **Номер станції:** {data.get('stNumber', 'Не вказано')}\n"
        f"📝 **Опис проблеми:** {data.get('description', 'Не вказано')}\n"
        f"✅ **Рішення:** {data.get('solution', 'Не вказано')}\n"
        f"🔧 **Виконані роботи:**\n$\n{work_done_text}\n$\n")

    # Перевіряємо, чи є фото
    if "photos" in data and data["photos"]:
        # Створюємо список InputMediaPhoto для кожного фото
        media = [InputMediaPhoto(media=photo) for photo in data["photos"]]

        # Відправляємо всі фото разом з першим звітом
        await message.answer_media_group(media=media
                                         )  # Відправляємо фото в групі
        await message.answer(report_text_1,
                             parse_mode="Markdown")  # Відправляємо текст звіту
    else:
        await message.answer(report_text_1, parse_mode="Markdown"
                             )  # Якщо фото немає, просто текст

    # Відправляємо друге повідомлення з роботами
    await message.answer(report_text_2, parse_mode="Markdown")

    await message.answer(
        "Звіт збережено. Ви можете надіслати його в бот або в service point.",
        reply_markup=kb_main)
    await state.clear()

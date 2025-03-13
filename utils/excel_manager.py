
import pandas as pd
import os
from openpyxl import load_workbook

class ExcelManager:
    def __init__(self, file_path="data/database.xlsx"):
        self.file_path = file_path
        # Перевіряємо, чи існує файл
        if not os.path.exists(file_path):
            # Створюємо порожній файл з двома листами
            writer = pd.ExcelWriter(file_path, engine='openpyxl')
            pd.DataFrame().to_excel(writer, sheet_name='Обладнання', index=False)
            pd.DataFrame().to_excel(writer, sheet_name='Звіти', index=False)
            writer.save()
    
    def get_equipment_list(self):
        """Отримати список обладнання"""
        try:
            df = pd.read_excel(self.file_path, sheet_name="Обладнання")
            return df
        except Exception as e:
            print(f"Помилка при читанні списку обладнання: {e}")
            return pd.DataFrame()
    
    def add_equipment(self, name, quantity, engineer=None):
        """Додати нове обладнання"""
        try:
            df = self.get_equipment_list()
            
            # Перевіряємо чи існує вже таке обладнання
            if name in df['Назва'].values:
                # Оновлюємо кількість
                idx = df[df['Назва'] == name].index[0]
                df.at[idx, 'Кількість'] = df.at[idx, 'Кількість'] + quantity
                if engineer and not pd.isna(engineer):
                    df.at[idx, 'Інженер'] = engineer
            else:
                # Додаємо нове обладнання
                new_row = pd.DataFrame({
                    'Назва': [name],
                    'Кількість': [quantity],
                    'Інженер': [engineer]
                })
                df = pd.concat([df, new_row], ignore_index=True)
            
            # Зберігаємо зміни, зберігаючи інші листи
            with pd.ExcelWriter(self.file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name="Обладнання", index=False)
            
            return True, "Обладнання успішно додано"
        except Exception as e:
            return False, f"Помилка при додаванні обладнання: {e}"
    
    def assign_equipment(self, name, engineer):
        """Призначити обладнання інженеру"""
        try:
            df = self.get_equipment_list()
            
            if name in df['Назва'].values:
                idx = df[df['Назва'] == name].index[0]
                df.at[idx, 'Інженер'] = engineer
                
                with pd.ExcelWriter(self.file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    df.to_excel(writer, sheet_name="Обладнання", index=False)
                
                return True, f"Обладнання {name} призначено інженеру {engineer}"
            else:
                return False, f"Обладнання {name} не знайдено"
        except Exception as e:
            return False, f"Помилка при призначенні обладнання: {e}"
    
    def save_report(self, engineer, date, station, works, distance, total_amount):
        """Зберегти звіт про виконану роботу"""
        try:
            # Зчитуємо існуючі звіти
            try:
                df = pd.read_excel(self.file_path, sheet_name="Звіти")
            except:
                # Якщо лист не існує, створюємо новий
                df = pd.DataFrame(columns=['Дата', 'Інженер', 'Станція', 'Роботи', 'Відстань', 'Сума'])
            
            # Додаємо новий звіт
            new_row = pd.DataFrame({
                'Дата': [date],
                'Інженер': [engineer],
                'Станція': [station],
                'Роботи': [', '.join(works)],
                'Відстань': [distance],
                'Сума': [total_amount]
            })
            
            df = pd.concat([df, new_row], ignore_index=True)
            
            # Зберігаємо дані
            with pd.ExcelWriter(self.file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name="Звіти", index=False)
            
            return True, "Звіт успішно збережено"
        except Exception as e:
            return False, f"Помилка при збереженні звіту: {e}"
    
    def get_engineer_reports(self, engineer=None):
        """Отримати звіти по інженеру"""
        try:
            df = pd.read_excel(self.file_path, sheet_name="Звіти")
            if engineer:
                df = df[df['Інженер'] == engineer]
            return df
        except Exception as e:
            print(f"Помилка при отриманні звітів: {e}")
            return pd.DataFrame()
    
    def calculate_salary(self, engineer, month=None):
        """Розрахувати зарплату інженера за місяць"""
        try:
            df = self.get_engineer_reports(engineer)
            
            if month:
                # Фільтруємо за місяцем, якщо вказано
                df['Дата'] = pd.to_datetime(df['Дата'])
                df = df[df['Дата'].dt.month == month]
            
            # Рахуємо загальну суму
            total_amount = df['Сума'].sum()
            
            return total_amount
        except Exception as e:
            print(f"Помилка при розрахунку зарплати: {e}")
            return 0

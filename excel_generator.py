# excel_generator.py faylida
import openpyxl
import os # os modulini qo'shing

def create_excel_file(data, user_id):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Arizalar"

    headers = ["Kalit", "Qiymat"]
    sheet.append(headers)

    for key, value in data.items():
        sheet.append([key, value])

    # Fayl nomini noyob qilish uchun user_id va vaqtni qo'shish
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S") # datetime import qilingan bo'lishi kerak
    file_name = f"ariza_{data.get('full_name', 'noma_lum').replace(' ', '_')}_{user_id}_{timestamp}.xlsx"
    workbook.save(file_name)
    return file_name

# datetime ni import qilishni unutmang
from datetime import datetime

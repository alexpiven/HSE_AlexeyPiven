from ics import Calendar
from datetime import datetime
from zoneinfo import ZoneInfo
import json

# Путь к вашему .ics файлу
file_path = 'А40-183194-2015.ics'

# Номер дела
case_number = 'А40-183194/2015'

# Читаем содержимое файла
with open(file_path, 'r', encoding='utf-8') as f:
    cal_data = f.read()

# Парсим календарь
c = Calendar(cal_data)

# Список для хранения данных о реальных заседаниях
court_sessions = []

for event in c.events:
    # Пропускаем пустые события
    if '00010101' in str(event.begin):
        continue

    # Проверяем, есть ли локация
    location = event.location.strip() if event.location else None
    if not location:
        continue

    # Формируем даты с временной зоной
    start_time = event.begin.to('Europe/Moscow').format('YYYY-MM-DDTHH:mm:ssZ')
    end_time = event.end.to('Europe/Moscow').format('YYYY-MM-DDTHH:mm:ssZ')

    # Описание
    description = event.description.strip() if event.description else ''

    # Добавляем в список
    court_sessions.append({
        'case_number': case_number,
        'start': start_time,
        'end': end_time,
        'location': location,
        'description': description
    })

# Сохраняем в JSON
with open('court_dates.json', 'w', encoding='utf-8') as f:
    json.dump(court_sessions, f, ensure_ascii=False, indent=2)

print(f"Найдено {len(court_sessions)} реальных заседаний. Сохранены в court_dates.json")
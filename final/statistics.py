# statistics.py

from typing import List, Dict, Any

def generate_statistics(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Генерирует статистику по судам и временам года внесения в реестр.
    Использует dict/list comprehensions.
    """
    # Статистика по судам
    court_stats = {
        court: len([item for item in data if item.get('court_name', '') == court])
        for court in set(item.get('court_name', '') for item in data)
    }
    # Сортировка по убыванию
    court_stats_sorted = dict(sorted(court_stats.items(), key=lambda x: x[1], reverse=True))

    # Статистика по временам года внесения в реестр
    # Сначала создаем словарь для времён года
    season_map = {
        'зима': [12, 1, 2],
        'весна': [3, 4, 5],
        'лето': [6, 7, 8],
        'осень': [9, 10, 11]
    }

    # Функция для определения сезона по месяцу
    def get_season(month: int) -> str:
        for season, months in season_map.items():
            if month in months:
                return season
        return 'неизвестно'

    # Считаем количество записей по сезонам
    # Проверяем, что дата не пустая и не 'неизвестно' перед разбиением
    season_stats = {}
    for season, months in season_map.items():
        count = 0
        for item in data:
            reg_date_str = item.get('registry_inclusion_date', '')
            if reg_date_str and reg_date_str != 'неизвестно':
                try:
                    # Разбиваем строку даты ISO (YYYY-MM-DD) и извлекаем месяц
                    date_parts = reg_date_str.split('-')
                    if len(date_parts) >= 2: # Убедимся, что есть год и месяц
                        month = int(date_parts[1])
                        if month in months:
                            count += 1
                except (ValueError, IndexError):
                    # Если формат даты некорректен, пропускаем этот элемент
                    continue
        season_stats[season] = count

    # Общая статистика
    total_records = len(data)
    records_with_court = len([item for item in data if item.get('court_name', '') and item.get('court_name', '') != 'неизвестно'])
    records_with_registry_date = len([item for item in data if item.get('registry_inclusion_date', '') and item.get('registry_inclusion_date', '') != 'неизвестно'])

    return {
        'total_records': total_records,
        'records_with_court': records_with_court,
        'records_with_registry_date': records_with_registry_date,
        'court_statistics': court_stats_sorted,
        'season_statistics': season_stats
    }
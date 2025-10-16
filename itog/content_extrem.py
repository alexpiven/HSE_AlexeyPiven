# content_extrem.py
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any


class ContentExtrem:
    """
    Класс для работы с собранными данными из реестра экстремистских материалов.
    """

    def __init__(self, data_file: str = 'parsed_data.json'):
        """
        Инициализирует экземпляр класса, загружая данные из JSON-файла.
        :param data_file: Путь к файлу с данными (parsed_data.json).
        """
        self.data_file = data_file
        self.data = self._load_data()

    def _load_data(self) -> List[Dict[str, Any]]:
        """
        Загружает данные из JSON-файла.
        :return: Список словарей с данными.
        """
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Данные в файле должны быть представлены в виде списка.")
            return data
        except FileNotFoundError:
            print(f"Файл {self.data_file} не найден.")
            return []
        except json.JSONDecodeError:
            print(f"Файл {self.data_file} содержит некорректный JSON.")
            return []
        except ValueError as e:
            print(f"Ошибка в структуре данных: {e}")
            return []
        except Exception as e:
            print(f"Неизвестная ошибка при загрузке данных: {e}")
            return []

    def ContentByCategory(self, content_type: str) -> List[Dict[str, Any]]:
        """
        Возвращает список материалов, относящихся к выбранной категории.
        :param content_type: Тип контента (например, 'видео', 'аудио', 'текст').
        :return: Список материалов (словарей).
        """
        # Предполагается, что в данных есть ключ 'content_type'
        result = []
        for item in self.data:
            # Проверяем, что ключ 'content_type' существует и его значение совпадает
            if item.get('content_type', '').lower() == content_type.lower():
                result.append(item)
        return result

    def RandomURLExtrem(self) -> str:
        """
        Возвращает случайный материал из реестра в формате "Описание/URL".
        :return: Строка в формате "Описание/URL" или сообщение, если URL нет.
        """
        # Отфильтруем элементы, у которых есть хотя бы один URL
        items_with_urls = [item for item in self.data if item.get('urls')]
        if not items_with_urls:
            return "Не найдено материалов с URL."

        # Выбираем случайный элемент
        random_item = random.choice(items_with_urls)

        description = random_item.get('description', 'Описание отсутствует')
        # Берем первый URL из списка, если список не пуст
        url = random_item['urls'][0] if random_item.get('urls') else 'URL отсутствует'

        return f"{description} / {url}"

    def ContentByCourt(self, court_name: str, year: int) -> List[Dict[str, Any]]:
        """
        Возвращает список материалов, внесенных в реестр на основании решения выбранного суда за конкретный год.
        :param court_name: Название суда (например, 'Верховный Суд').
        :param year: Год (например, 2023).
        :return: Список материалов (словарей).
        """
        result = []
        # Предполагается, что в данных есть ключи 'court_name' и 'court_decision_date'
        for item in self.data:
            item_court_name = item.get('court_name', '').lower()
            court_date_str = item.get('court_decision_date')

            # Проверяем, совпадает ли название суда (без учета регистра)
            court_match = court_name.lower() in item_court_name or item_court_name in court_name.lower()

            # Проверяем, совпадает ли год
            year_match = False
            if court_date_str and court_date_str != 'неизвестно':
                try:
                    court_date = datetime.fromisoformat(court_date_str)
                    if court_date.year == year:
                        year_match = True
                except ValueError:
                    # Если формат даты некорректен, пропускаем этот элемент
                    continue

            if court_match and year_match:
                result.append(item)

        return result

    def LastExtrem(self) -> List[Dict[str, Any]]:
        """
        Возвращает список материалов, внесенных в реестр за последний месяц.
        :return: Список материалов (словарей).
        """
        result = []
        one_month_ago = datetime.now() - timedelta(days=30)

        for item in self.data:
            registry_date_str = item.get('registry_inclusion_date')

            if registry_date_str and registry_date_str != 'неизвестно':
                try:
                    # Предполагается, что дата в формате ISO 8601 (YYYY-MM-DD)
                    registry_date = datetime.fromisoformat(registry_date_str)
                    if registry_date >= one_month_ago:
                        result.append(item)
                except ValueError:
                    # Если формат даты некорректен, пропускаем этот элемент
                    continue

        return result

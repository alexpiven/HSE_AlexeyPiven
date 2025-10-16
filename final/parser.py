import re
import json
import os
from typing import List, Dict, Any
from datetime import datetime

# Импортируем словарь категорий из отдельного файла
from content_categories import CONTENT_CATEGORIES

class ParserExtrem:
    # Константы для путей
    INPUT_DIR = 'data'
    OUTPUT_FILE = 'parsed_data.json'

    def __init__(self, input_dir: str = None, output_file: str = None):
        """
        Инициализирует парсер.
        :param input_dir: Директория с CSV-файлами. Если не указана, используется значение по умолчанию.
        :param output_file: Файл для вывода JSON. Если не указан, используется значение по умолчанию.
        """
        self.input_dir = input_dir if input_dir is not None else self.INPUT_DIR
        self.output_file = output_file if output_file is not None else self.OUTPUT_FILE

    def categorize_content(self, description: str) -> str:
        """Определяет категорию контента на основе описания."""
        description_lower = description.lower()
        for category, keywords in CONTENT_CATEGORIES.items():
            if any(keyword in description_lower for keyword in keywords):
                return category
        return 'неопределено'

    def extract_urls(self, text: str) -> List[str]:
        """Извлекает все URL-адреса из текста."""
        # Улучшенное регулярное выражение для URL
        url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
        urls = re.findall(url_pattern, text)
        # Очистка от лишних символов в конце (часто встречается в данных)
        cleaned_urls = [url.rstrip('.,;:!?)]}>"\'') for url in urls]
        return list(set(cleaned_urls))  # Удаление дубликатов

    def extract_court_and_date(self, text: str) -> tuple:
        """
        Извлекает название суда (в именительном падеже) и дату решения суда из текста.
        Возвращает кортеж: (название_суда, дата_решения)
        """
        # Шаблон для поиска "(решение ... от ДД.ММ.ГГГГ)"
        # Ищем "решение", затем любые символы (нежадно), затем "от", затем дату.
        court_date_pattern = r'\(решение\s+(.+?)\s+от\s+(\d{2}\.\d{2}\.\d{4})'
        match = re.search(court_date_pattern, text)

        if not match:
            return '', ''

        full_court_text = match.group(1).strip()
        court_date = match.group(2)

        # Приведение к именительному падежу
        # Создаем словарь для замены окончаний
        case_endings = {
            'суда': 'суд',
            'ного': 'ный',
            'ого': 'ий',
            'его': 'евый',
            'го': 'й',
            'ей': 'ая',  # Для женского рода
            'ой': 'ая',  # Для женского рода
            'ых': 'ые',  # Для множественного числа
            'их': 'ие',  # Для множественного числа
            'ом': 'ым',   # Для творительного падежа
            'ем': 'ым',   # Для творительного падежа
            'ами': 'ыми', # Для творительного падежа
            'ями': 'ыми', # Для творительного падежа
            'ую': 'ую',   # Для винительного падежа женского рода
            'ю': 'ю',     # Для винительного падежа
            'и': 'и',     # Для множественного числа
            'е': 'е',     # Для предложного падежа
            'у': 'у',     # Для винительного падежа
            'я': 'я',     # Для винительного падежа
            'ь': 'ь',     # Для мягкого знака
        }


        court_name = full_court_text

        # Убираем возможные слова, которые могут быть в конце описания суда.
        court_name = re.sub(r'\s*(?:и\s*определение|по\s*гражданским\s*делам|по\s*административным\s*делам|судебной\s*коллегии|апелляционное\s*определение|кассационное\s*определение|заочное\s*решение)\s*', ' ', court_name)

        # Убираем лишние пробелы
        court_name = ' '.join(court_name.split()).strip()

        # Убираем возможные остатки скобок или знаков препинания в конце
        court_name = court_name.rstrip(' .,;:()[]{}')

        # Попробуем убрать "от" и "суда" в начале/конце, если они есть
        court_name = re.sub(r'^\s*(?:от|суда)\s*', '', court_name)
        court_name = re.sub(r'\s*(?:от|суда)\s*$', '', court_name)

        # Если название слишком длинное или содержит "от", возможно, мы не смогли его полностью очистить.
        # В таком случае, можно просто вернуть то, что нашли, без дополнительной очистки.
        # Для большей точности потребуется NLP, но это выходит за рамки простого регэкспа.

        # Попробуем привести к именительному падежу с помощью словаря окончаний
        # Разбиваем название на слова
        words = court_name.split()
        new_words = []

        for word in words:
            # Проверяем, является ли слово прилагательным или существительным
            # Если слово заканчивается на одно из окончаний, заменяем его
            for ending, replacement in case_endings.items():
                if word.endswith(ending):
                    # Заменяем окончание
                    new_word = word[:-len(ending)] + replacement
                    new_words.append(new_word)
                    break
            else:
                # Если не нашли подходящего окончания, оставляем слово как есть
                new_words.append(word)

        # Собираем обратно в строку
        court_name = ' '.join(new_words)

        # Возвращаем результат
        return court_name, court_date

    def extract_registry_date(self, text: str) -> str:
        """Извлекает дату включения в реестр из конца строки."""
        date_pattern = r'(\d{2}\.\d{2}\.\d{4})$'
        match = re.search(date_pattern, text.strip())
        return match.group(1) if match else ''

    def parse_line(self, line: str) -> Dict[str, Any]:
        """Парсит одну строку из CSV-файла."""
        # Разделяем строку по первому символу ';'
        parts = line.split(';', 1)
        if len(parts) < 2:
            return None

        record_number = parts[0].strip()
        description_part = parts[1].strip()

        # Извлекаем описание материала и дату включения в реестр
        # Дата включения обычно находится в конце, отделенная от описания ';'
        description_parts = description_part.rsplit(';', 1)
        description = description_parts[0].strip()
        registry_date = self.extract_registry_date(description_part)  # Извлекаем дату включения из всей строки

        # Определяем категорию контента
        content_type = self.categorize_content(description)

        # Извлекаем URL-адреса
        urls = self.extract_urls(description)

        # Извлекаем название суда и дату его решения
        court_name, court_date = self.extract_court_and_date(description)

        # Приводим данные к рабочим типам
        # Даты приводим к формату ISO8601
        try:
            registry_date_iso = datetime.strptime(registry_date, '%d.%m.%Y').strftime('%Y-%m-%d') if registry_date else ''
        except ValueError:
            registry_date_iso = ''

        try:
            court_date_iso = datetime.strptime(court_date, '%d.%m.%Y').strftime('%Y-%m-%d') if court_date else ''
        except ValueError:
            court_date_iso = ''

        # Заполняем пробелы в данных
        # Если данные отсутствуют, используем значения по умолчанию
        if not record_number:
            record_number = 'неизвестно'
        if not content_type:
            content_type = 'неопределено'
        if not description:
            description = 'описание отсутствует'
        if not urls:
            urls = []
        if not court_name:
            court_name = 'неизвестно'
        if not court_date_iso:
            court_date_iso = 'неизвестно'
        if not registry_date_iso:
            registry_date_iso = 'неизвестно'

        return {
            'record_number': record_number,
            'content_type': content_type,
            'description': description,
            'urls': urls,
            'court_name': court_name,
            'court_decision_date': court_date_iso,  # Новая переменная для даты решения суда
            'registry_inclusion_date': registry_date_iso  # Переименовано для ясности
        }

    def serialize_to_json(self, data: List[Dict[str, Any]], filename: str) -> None:
        """Сериализует данные в JSON-файл."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Данные успешно сериализованы в {filename}")
        except Exception as e:
            print(f"Ошибка при сериализации: {e}")

    def deserialize_from_json(self, filename: str) -> List[Dict[str, Any]]:
        """Десериализует данные из JSON-файла."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"Данные успешно десериализованы из {filename}")
            return data
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")
            return []
        except Exception as e:
            print(f"Ошибка при десериализации: {e}")
            return []

    def get_latest_csv_file(self, directory: str) -> str:
        """Находит последний добавленный CSV-файл в указанной директории."""
        try:
            # Получаем список всех файлов .csv в директории
            csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
            if not csv_files:
                raise FileNotFoundError("В папке /data не найдено ни одного файла с расширением .csv")

            # Сортируем файлы по времени последнего изменения (mtime), берем последний
            latest_file = max(csv_files, key=lambda f: os.path.getmtime(os.path.join(directory, f)))
            return os.path.join(directory, latest_file)
        except Exception as e:
            print(f"Ошибка при поиске последнего CSV-файла: {e}")
            return ""

    def start(self):
        """Основной метод для запуска парсера."""
        # Находим последний CSV-файл
        input_file = self.get_latest_csv_file(self.input_dir)
        if not input_file:
            return

        parsed_data = []

        # Читаем и парсим файл
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for i, line in enumerate(lines, 1):
                    line = line.strip()
                    if line:  # Пропускаем пустые строки
                        parsed_record = self.parse_line(line)
                        if parsed_record:
                            parsed_data.append(parsed_record)
                        else:
                            print(f"Предупреждение: Не удалось распарсить строку {i}: {line[:100]}...")
        except Exception as e:
            print(f"Ошибка при чтении файла {input_file}: {e}")
            return

        # Сериализуем данные в JSON
        self.serialize_to_json(parsed_data, self.output_file)


# Пример использования:
if __name__ == "__main__":
     parser = ParserExtrem()
     parser.start()

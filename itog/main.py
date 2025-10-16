# main.py

import os
import json
import sys
from loader import download_file, DOWNLOAD_URL, DATA_DIR
from parser import ParserExtrem
from statistics import generate_statistics
from content_extrem import ContentExtrem

# Импортируем словарь категорий для отображения в подсказке
from content_categories import CONTENT_CATEGORIES


def main():
    print("=== Программа обработки реестра экстремистских материалов ===\n")

    # Шаг 1: Скачивание последнего CSV-файла
    print("1. Скачивание последнего CSV-файла...")
    try:
        csv_file_path = download_file(DOWNLOAD_URL, DATA_DIR)  # Вызов функции из loader.py
        if not csv_file_path:
            print("❌ Не удалось скачать файл. Программа завершена.")
            return
        print(f"✅ Файл успешно скачан: {csv_file_path}\n")
    except Exception as e:
        print(f"❌ Ошибка при скачивании файла: {e}")
        return

    # Шаг 2: Парсинг данных
    print("2. Парсинг данных из CSV-файла...")
    try:
        parser = ParserExtrem()
        parser.start()
        print("✅ Данные успешно распарсены и сохранены в parsed_data.json\n")
    except Exception as e:
        print(f"❌ Ошибка при парсинге данных: {e}")
        return

    # Шаг 3: Загрузка распарсенных данных и генерация статистики
    print("3. Загрузка данных и генерация статистики...")
    try:
        # Загружаем данные из файла, который создал парсер
        with open('parsed_data.json', 'r', encoding='utf-8') as f:
            parsed_data = json.load(f)

        stats = generate_statistics(parsed_data)  # Вызов функции из statistics.py
        print("✅ Статистика успешно сгенерирована:")
        print(f"   - Всего записей: {stats.get('total_records', 'N/A')}")
        print(f"   - Записей с указанием суда: {stats.get('records_with_court', 'N/A')}")
        print(f"   - Записей с датой включения: {stats.get('records_with_registry_date', 'N/A')}")
        print("   - Статистика по судам (топ-5):")
        for court, count in list(stats.get('court_statistics', {}).items())[:5]:
            print(f"     * {court}: {count}")
        print("   - Статистика по сезонам:")
        for season, count in stats.get('season_statistics', {}).items():
            print(f"     * {season}: {count}")
        print()
    except FileNotFoundError:
        print("❌ Файл parsed_data.json не найден. Убедитесь, что парсер завершил работу успешно.")
        return
    except json.JSONDecodeError:
        print("❌ Файл parsed_data.json содержит некорректный JSON.")
        return
    except Exception as e:
        print(f"❌ Ошибка при генерации статистики: {e}")
        return

    # Шаг 4: Интерактивное меню
    print("4. Запуск интерактивного меню...\n")
    # ContentExtrem по умолчанию загружает 'parsed_data.json'
    content_manager = ContentExtrem()

    while True:
        print("\n" + "=" * 50)
        print("Выберите действие:")
        print("1. Показать материалы по категории")
        print("2. Получить случайный материал (Описание/URL)")
        print("3. Показать материалы по суду и году")
        print("4. Показать материалы за последний месяц")
        print("5. Выход")
        print("=" * 50)

        choice = input("Введите номер действия (1-5): ").strip()

        if choice == '1':
            # Выводим список доступных категорий
            available_categories = list(CONTENT_CATEGORIES.keys())
            print(f"Доступные категории: {', '.join(available_categories)}")
            category = input("Введите категорию (точно как в списке выше): ").strip()
            results = content_manager.ContentByCategory(category)
            print(f"\nНайдено материалов в категории '{category}': {len(results)}")
            for item in results[:10]:  # Выводим первые 10 для краткости
                print(f" - {item.get('description', 'Без описания')}")
            if len(results) > 10:
                print(f" ... и еще {len(results) - 10} материалов.")

        elif choice == '2':
            random_item = content_manager.RandomURLExtrem()
            print(f"\nСлучайный материал:\n{random_item}")

        elif choice == '3':
            # Загружаем список уникальных судов из parsed_data.json
            try:
                with open('parsed_data.json', 'r', encoding='utf-8') as f:
                    parsed_data_for_courts = json.load(f)

                # Извлекаем все уникальные имена судов, исключая 'неизвестно'
                all_courts = set()
                for item in parsed_data_for_courts:
                    court_name = item.get('court_name', 'неизвестно')
                    if court_name and court_name != 'неизвестно':
                        all_courts.add(court_name)

                if all_courts:
                    print(f"Известные суды (первые 10): {', '.join(list(all_courts)[:10])}")
                    if len(all_courts) > 10:
                        print(f" ... и еще {len(all_courts) - 10} судов.")
                else:
                    print("Суды в данных не найдены.")
            except FileNotFoundError:
                print("❌ Файл parsed_data.json не найден для получения списка судов.")
            except json.JSONDecodeError:
                print("❌ Файл parsed_data.json содержит некорректный JSON.")
            except Exception as e:
                print(f"❌ Ошибка при загрузке списка судов: {e}")

            court_name = input("Введите название суда (точно как в списке выше): ").strip()
            year_input = input("Введите год (например, 2023): ").strip()
            try:
                year = int(year_input)
                results = content_manager.ContentByCourt(court_name, year)
                print(f"\nНайдено материалов по суду '{court_name}' за {year} год: {len(results)}")
                for item in results[:10]:
                    print(
                        f" - {item.get('description', 'Без описания')} (Дата решения: {item.get('court_decision_date', 'Неизвестно')})")
                if len(results) > 10:
                    print(f" ... и еще {len(results) - 10} материалов.")
            except ValueError:
                print("❌ Неверный формат года. Введите целое число.")

        elif choice == '4':
            results = content_manager.LastExtrem()
            print(f"\nНайдено материалов за последний месяц: {len(results)}")
            for item in results[:10]:
                print(
                    f" - {item.get('description', 'Без описания')} (Дата включения: {item.get('registry_inclusion_date', 'Неизвестно')})")
            if len(results) > 10:
                print(f" ... и еще {len(results) - 10} материалов.")

        elif choice == '5':
            print("\nДо свидания!")
            break

        else:
            print("\n❌ Неверный выбор. Пожалуйста, выберите число от 1 до 5.")

        # Задержка перед следующим выводом меню - ждем нажатия Enter
        print("\nНажмите Enter, чтобы вернуться в меню...", end='', flush=True)
        sys.stdin.readline()  # Читает оставшиеся символы до и включая \n


if __name__ == "__main__":
    main()
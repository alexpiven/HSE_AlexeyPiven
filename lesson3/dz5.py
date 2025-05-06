import json
import csv
import re

TXT_TRADERS_PATH = 'traders.txt'
JSON_TRADERS_PATH = 'traders.json'
JSON_EFRSB_PATH = '1000_efrsb_messages.json'

def save_emails_to_json(email_dict, output_file='emails.json'):
    """
    Сохраняет словарь с email-адресами в JSON-файл.
    Преобразует множества в списки для сериализации.

    :param email_dict: Словарь {inn: set(emails)}
    :param output_file: Имя выходного JSON-файла
    """
    try:
        # Преобразуем множества в списки для JSON
        serializable = {inn: list(emails) for inn, emails in email_dict.items()}

        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            json.dump(serializable, f, ensure_ascii=False, indent=4) # type: ignore
        print(f"Email-адреса успешно сохранены в файл '{output_file}'.")
    except Exception as e:
        print(f"Ошибка при записи в JSON: {e}")

def collect_emails_by_inn(json_file_path, search_fields=None):
    """
    Считывает JSON-файл и находит email-адреса в указанных полях.
    Группирует найденные адреса по 'publisher_inn'.

    :param json_file_path: Путь к JSON-файлу
    :param search_fields: Список полей для поиска email (например: ['msg_text', 'contact_info'])
                          Если None — используются все строковые поля, кроме 'publisher_inn'
    :return: Словарь {inn: set(emails)}
    """
    result = {}

    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            for entry in data:
                inn = entry.get("publisher_inn")
                if not inn:
                    continue

                # Собрать текст из нужных полей
                full_text = ''
                if search_fields is None:
                    # Искать во всех полях, кроме publisher_inn
                    for key, value in entry.items():
                        if key != "publisher_inn" and isinstance(value, str):
                            full_text += ' ' + value
                else:
                    # Искать только в указанных полях
                    for field in search_fields:
                        value = entry.get(field, '')
                        if isinstance(value, str):
                            full_text += ' ' + value

                emails = find_emails(full_text)
                if emails:
                    if inn not in result:
                        result[inn] = set()
                    result[inn].update(emails)

    except FileNotFoundError:
        print(f"Ошибка: файл '{json_file_path}' не найден.")
    except json.JSONDecodeError:
        print("Ошибка: файл не является корректным JSON.")

    return result

def find_emails(text):
    """
    Находит все email-адреса в переданной строке.

    :param text: Текст для поиска email-адресов
    :return: Список найденных email-адресов
    """
    # Регулярное выражение для email
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    emails = re.findall(email_pattern, text)
    return emails

def save_traders_to_csv(records, output_file='traders.csv'):
    """
    Сохраняет список записей в CSV-файл.

    :param records: Список словарей с ключами 'inn', 'ogrn', 'address'
    :param output_file: Имя выходного CSV-файла
    """
    if not records:
        print("Нет данных для сохранения.")
        return

    fieldnames = ['inn', 'ogrn', 'address']

    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames) # type: ignore
            writer.writeheader()
            writer.writerows(records)
        print(f"Данные успешно сохранены в файл '{output_file}'.")
    except Exception as e:
        print(f"Ошибка при записи в CSV: {e}")

def find_traders_by_inn(json_path, inn_list):
    """
    Находит записи по списку ИНН в JSON-файле.

    :param json_path: Путь к JSON-файлу с данными организаций
    :param inn_list: Список ИНН для поиска
    :return: Список словарей с полями inn, ogrn, address
    """
    found_records = []

    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            traders = json.load(file)

            # Предполагаем, что traders — это список словарей
            for trader in traders:
                if trader.get('inn') in inn_list:
                    record = {
                        'inn': trader['inn'],
                        'ogrn': trader.get('ogrn', ''),
                        'address': trader.get('address', '')
                    }
                    found_records.append(record)

    except FileNotFoundError:
        print(f"Ошибка: файл '{json_path}' не найден.")
    except json.JSONDecodeError:
        print("Ошибка: файл не является корректным JSON.")

    return found_records

def inn_from_txt(txt_path):
    """
       Считывает файл и возвращает список ИНН, исключая пустые строки.

       :param txt_path: Путь к текстовому файлу с ИНН
       :return: Список ИНН (с типом str)
    """

    inn_list = []
    try:
        with open(txt_path, 'r', encoding='utf-8') as file:
            inn_list = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Ошибка: файл '{txt_path}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")

    return inn_list

def main():
    # Шаг 1: Формируем список ИНН организаций из traders.txt
    inn_list = inn_from_txt(TXT_TRADERS_PATH)
    if not inn_list:
        print("Не найдено ИНН для поиска.")
        return

    # Шаг 2: Найти организации в traders.json
    traders_data = find_traders_by_inn(JSON_TRADERS_PATH, inn_list)
    if not traders_data:
        print("Организации по указанным ИНН не найдены.")
        return

    # Шаг 3: Сохранить результат в CSV
    save_traders_to_csv(traders_data)

    # Шаг 4: Найти e-mail адреса в 1000_efrsb_messages.json
    email_data = collect_emails_by_inn(JSON_EFRSB_PATH)
    if not email_data:
        print("Email-адреса не найдены.")
        return

    # Шаг 5: Сохранить результат в JSON
    save_emails_to_json(email_data)

if __name__ == "__main__":
    main()
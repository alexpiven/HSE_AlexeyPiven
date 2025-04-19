import time
from lesson_2_data import respondents
from lesson_2_data import courts


def gen_court_header(court):
    """
    Функция для генерации заголовка суда.
    :param court: Словарь с данными суда (например, {'court_code': '123', 'court_name': 'Московский городской суд'}).
    :return: Строка с заголовком суда.
    """
    # Формируем строку заголовка суда на основе его названия
    header = f"В: {court['court_name']} \n"
    return header


def gen_istec_header():
    """
    Функция для генерации заголовка истца.
    :return: Строка с информацией об истце.
    """
    # Формируем строку заголовка истца с его ИНН, ОГРН и адресом
    header = f"Истец: Пупкин Василий Геннадьевич\n" \
             f"ИНН  1236182357 ОГРН  218431927812733 \n" \
             f"Адрес: 123534, г. Москва, ул. Водников, 13 \n"
    return header


def gen_respondent_header(respondent):
    """
    Функция для генерации заголовка ответчика.
    :param respondent: Словарь с данными ответчика (например, {'short_name': 'ООО "Ромашка"', 'inn': '1234567890', ...}).
    :return: Строка с информацией об ответчике.
    """
    # Формируем строку заголовка ответчика с его названием, ИНН, ОГРН, адресом и номером дела
    header = f"Ответчик: {respondent['short_name']} \n" \
             f"ИНН  {respondent['inn']} ОГРН {respondent['ogrn']}  \n" \
             f"Адрес: {respondent['address']} \n" \
             f"Номер дела: {respondent['case_number']} \n"
    return header


def process_respondents(respondents_list, courts_list):
    """
    Функция для обработки списка ответчиков и генерации шапок документов.
    :param respondents_list: Список словарей с данными ответчиков.
    :param courts_list: Список словарей с данными судов.
    """
    # Создаем словарь для быстрого поиска суда по коду
    court_mapping = {court['court_code']: court for court in courts_list}

    # Обработка данных для каждого ответчика
    for respondent in respondents_list:
        try:
            # Извлекаем код суда из первых трёх символов номера дела
            code = respondent['case_number'][:3]
            court = court_mapping[code]

            # Генерация заголовков
            court_header = gen_court_header(court=court)
            print(court_header)
            istec_header = gen_istec_header()
            print(istec_header)
            respondent_header = gen_respondent_header(respondent=respondent)
            print(respondent_header)

        except Exception as e:
            # Если возникает ошибка (например, отсутствует ключ или данные некорректны),
            # выводим сообщение об ошибке и продолжаем работу с остальными ответчиками
            print(f'Ошибка при обработке данных: {e}')
            continue


def main():
    """
    Основная функция программы.
    """
    print('start')

    # Вызов функции для обработки данных ответчиков и судов
    process_respondents(respondents_list=respondents, courts_list=courts)

    print('stop')


if __name__ == "__main__":
    # Точка входа в программу
    main()
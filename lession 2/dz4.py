def validate_inn(inn):
    """
    Основная функция для валидации ИНН.
    :param inn: строка, содержащая ИНН
    :return: True, если ИНН валиден, иначе False
    """
    # Проверяем, что входные данные состоят только из цифр
    if not inn.isdigit():
        return False

    # Проверяем длину ИНН
    if len(inn) == 10:
        return validate_inn_organization(inn)
    elif len(inn) == 12:
        return validate_inn_individual(inn)
    else:
        return False


def validate_inn_organization(inn):
    """
    Валидация ИНН организации (10 цифр).
    :param inn: строка, содержащая ИНН организации
    :return: True, если ИНН валиден, иначе False
    """
    # Коэффициенты для проверки контрольного числа
    coefficients = [2, 4, 10, 3, 5, 9, 4, 6, 8]

    # Вычисляем контрольную сумму
    control_sum = sum(int(inn[i]) * coefficients[i] for i in range(9))

    # Вычисляем контрольное число
    control_number = control_sum % 11
    if control_number > 9:
        control_number %= 10

    # Сравниваем контрольное число с последней цифрой ИНН
    return control_number == int(inn[9])


def validate_inn_individual(inn):
    """
    Валидация ИНН физического лица или ИП (12 цифр).
    :param inn: строка, содержащая ИНН физического лица или ИП
    :return: True, если ИНН валиден, иначе False
    """
    # Коэффициенты для первого контрольного числа
    coefficients_1 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]

    # Коэффициенты для второго контрольного числа
    coefficients_2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]

    # Вычисляем первую контрольную сумму
    control_sum_1 = sum(int(inn[i]) * coefficients_1[i] for i in range(10))
    control_number_1 = control_sum_1 % 11
    if control_number_1 > 9:
        control_number_1 %= 10

    # Вычисляем вторую контрольную сумму
    control_sum_2 = sum(int(inn[i]) * coefficients_2[i] for i in range(11))
    control_number_2 = control_sum_2 % 11
    if control_number_2 > 9:
        control_number_2 %= 10

    # Сравниваем контрольные числа с соответствующими цифрами ИНН
    return (control_number_1 == int(inn[10])) and (control_number_2 == int(inn[11]))


# Пример использования
if __name__ == "__main__":
    test_inns = [
        "7704352710",  # Валидный ИНН организации
        "7704352711",  # Невалидный ИНН организации
        "366406939712",  # Валидный ИНН физического лица
        "366406939713",  # Невалидный ИНН физического лица
        "abc123",  # Невалидный формат
        "1234567890123"  # Неверная длина
    ]

    for inn in test_inns:
        print(f"ИНН: {inn}, Валиден: {validate_inn(inn)}")
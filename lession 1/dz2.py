# Создаем пустой список для хранения участников
participants = []

# Запрашиваем количество участников
while True:
    try:
        num_participants = int(input("Введите количество участников: "))
        if num_participants > 0:
            break
        else:
            print("Количество участников должно быть больше 0!")
    except ValueError:
        print("Ошибка: введите целое число!")

# Запрашиваем данные для каждого участника
for i in range(num_participants):
    print(f"\nВведите данные для участника {i + 1}:")

    # Запрашиваем наименование
    while True:
        name = input("Наименование: ")
        if name.strip():  # Проверяем, что строка не пустая
            break
        else:
            print("Наименование не может быть пустым!")

    # Запрашиваем статус
    while True:
        status = input("Статус (например, 'Истец', 'Ответчик', 'Третье лицо'): ")
        if status.strip():  # Проверяем, что строка не пустая
            break
        else:
            print("Статус не может быть пустым!")

    # Запрашиваем ИНН
    while True:
        inn = input("ИНН: ")
        if inn.isdigit() and len(inn) >= 10:  # Проверяем, что ИНН состоит из цифр и имеет длину >= 10
            break
        else:
            print("ИНН должен содержать только цифры и иметь длину не менее 10 символов!")

    # Создаем словарь для текущего участника
    participant = {
        "name": name,
        "status": status,
        "inn": inn
    }

    # Добавляем словарь в список
    participants.append(participant)

# Выводим полученные данные в консоль в удобном формате
print("\nГотовая структура данных:")
for i, participant in enumerate(participants, start=1):
    print(f"Участник {i}:")
    print(f"  Наименование: {participant['name']}")
    print(f"  Статус: {participant['status']}")
    print(f"  ИНН: {participant['inn']}")
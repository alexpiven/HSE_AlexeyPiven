import random
import time


# 1. Генерируем отсортированный массив с случайным шагом
def generate_sorted_array():
    """Генерирует отсортированный массив от 10 до 250 млн с случайным шагом"""
    array = []
    current = 10
    step = random.randint(3, 5)  # случайный шаг от 3 до 5

    while current <= 250000000:
        array.append(current)
        current += step
        # Случайно меняем шаг для большей рандомизации
        if random.randint(1, 10) <= 3:  # 30% шанс изменить шаг
            step = random.randint(3, 5)

    return array


# Генерируем массив
print("Генерируем массив...")
sorted_array = generate_sorted_array()
print(f"Размер массива: {len(sorted_array)}")
print(f"Первые 10 элементов: {sorted_array[:10]}")
print(f"Последние 10 элементов: {sorted_array[-10:]}")

# 2. Генерируем 10 случайных чисел для поиска
random_numbers = [random.randint(1, 300000000) for _ in range(10)]
print(f"\nСлучайные числа для поиска: {random_numbers}")


# 3. Функция линейного поиска
def linear_search(arr, target):
    """Линейный поиск элемента в массиве"""
    for i in range(len(arr)):
        if arr[i] == target:
            return i  # возвращаем индекс найденного элемента
        elif arr[i] > target:
            break  # если массив отсортирован, можно остановиться
    return -1  # элемент не найден


# 4. Функция бинарного поиска
def binary_search(arr, target):
    """Бинарный поиск элемента в отсортированном массиве"""
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid  # элемент найден
        elif arr[mid] < target:
            left = mid + 1  # ищем в правой половине
        else:
            right = mid - 1  # ищем в левой половине

    return -1  # элемент не найден


# 5. Проверяем поиск и замеряем время
print("\nРезультаты поиска:")

# Для каждого случайного числа проверяем оба алгоритма
for num in random_numbers:
    # Линейный поиск
    start_time = time.time()
    result_linear = linear_search(sorted_array, num)
    linear_time = time.time() - start_time

    # Бинарный поиск
    start_time = time.time()
    result_binary = binary_search(sorted_array, num)
    binary_time = time.time() - start_time

    # Выводим результаты
    print(f"\nЧисло {num}:")
    if result_linear != -1:
        print(f"  Найдено на позиции {result_linear}")
        print(f"  Линейный поиск: {linear_time:.6f} секунд")
        print(f"  Бинарный поиск: {binary_time:.6f} секунд")
        print(f"  Бинарный поиск быстрее в {linear_time / binary_time:.2f} раз" if binary_time > 0 else "")
    else:
        print(f"  Не найдено")
        print(f"  Линейный поиск: {linear_time:.6f} секунд")
        print(f"  Бинарный поиск: {binary_time:.6f} секунд")

# Дополнительные тесты для чисел, которые точно есть в массиве
print("\n" + "=" * 50)
print("Тест для чисел, которые точно есть в массиве:")

# Берем несколько чисел из массива
test_numbers = sorted_array[::len(sorted_array) // 5][:5]  # 5 чисел из массива

for num in test_numbers:
    # Линейный поиск
    start_time = time.time()
    result_linear = linear_search(sorted_array, num)
    linear_time = time.time() - start_time

    # Бинарный поиск
    start_time = time.time()
    result_binary = binary_search(sorted_array, num)
    binary_time = time.time() - start_time

    # Выводим результаты
    print(f"\nЧисло {num}:")
    print(f"  Позиция: {result_linear}")
    print(f"  Линейный поиск: {linear_time:.6f} секунд")
    print(f"  Бинарный поиск: {binary_time:.6f} секунд")
    if binary_time > 0:
        print(f"  Бинарный поиск быстрее в {linear_time / binary_time:.2f} раз")
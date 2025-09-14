import random
import time

# 1. Генерируем массив из целых чисел, содержащий 100 000 элементов
print("Генерируем первый массив из 100 000 целых чисел...")
array_1 = [random.randint(1, 1000000) for _ in range(100000)]
print(f"Первый массив сгенерирован. Первые 10 элементов: {array_1[:10]}")

# 2. Генерируем массив словарей с длиной 100 000 элементов
print("Генерируем второй массив из 100 000 словарей...")
array_2 = [
    {
        "num_1": random.randint(1, 1000000),
        "num_2": random.randint(1, 1000000)
    }
    for _ in range(100000)
]
print(f"Второй массив сгенерирован. Первые 3 элемента: {array_2[:3]}")


# 3. Функция алгоритма сортировки пузырьком
def bubble_sort(arr):
    """Сортировка пузырьком"""
    n = len(arr)
    # Создаем копию массива, чтобы не изменять оригинальный
    arr_copy = arr.copy()

    for i in range(n):
        # Флаг для оптимизации - если не было обменов, массив отсортирован
        swapped = False
        for j in range(0, n - i - 1):
            if arr_copy[j] > arr_copy[j + 1]:
                # Меняем элементы местами
                arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                swapped = True
        # Если не было обменов, выходим из цикла
        if not swapped:
            break

    return arr_copy


# Сортируем первый массив (покажем на маленьком примере из-за медленной скорости пузырька)
print("\nСортируем первый массив алгоритмом пузырьком (на примере первых 100 элементов)...")
small_array = array_1[:100]  # Берем только первые 100 элементов для демонстрации
start_time = time.time()
sorted_bubble = bubble_sort(small_array)
bubble_time = time.time() - start_time
print(f"Первые 10 отсортированных элементов пузырьком: {sorted_bubble[:10]}")
print(f"Время сортировки пузырьком (100 элементов): {bubble_time:.6f} секунд")

# Для сравнения используем встроенную сортировку на полном массиве
print("Сортируем первый массив встроенным методом sort()...")
start_time = time.time()
array_1_sorted = sorted(array_1)
builtin_time = time.time() - start_time
print(f"Первые 10 отсортированных элементов встроенным методом: {array_1_sorted[:10]}")
print(f"Время встроенной сортировки (100 000 элементов): {builtin_time:.6f} секунд")

# 4. Сортируем второй массив с помощью встроенного метода .sort() и лямбда-функции
print("\nСортируем второй массив по полю 'num_1'...")
start_time = time.time()
array_2_sorted_by_num1 = sorted(array_2, key=lambda x: x["num_1"])
sort_time_1 = time.time() - start_time
print(f"Первые 3 элемента, отсортированные по num_1: {array_2_sorted_by_num1[:3]}")
print(f"Время сортировки по num_1: {sort_time_1:.6f} секунд")

print("\nСортируем второй массив по полю 'num_2'...")
start_time = time.time()
array_2_sorted_by_num2 = sorted(array_2, key=lambda x: x["num_2"])
sort_time_2 = time.time() - start_time
print(f"Первые 3 элемента, отсортированные по num_2: {array_2_sorted_by_num2[:3]}")
print(f"Время сортировки по num_2: {sort_time_2:.6f} секунд")

# Сортировка по двум полям сразу
print("\nСортируем второй массив сначала по 'num_1', затем по 'num_2'...")
start_time = time.time()
array_2_sorted_double = sorted(array_2, key=lambda x: (x["num_1"], x["num_2"]))
sort_time_3 = time.time() - start_time
print(f"Первые 3 элемента, отсортированные по двум полям: {array_2_sorted_double[:3]}")
print(f"Время сортировки по двум полям: {sort_time_3:.6f} секунд")

# Дополнительная демонстрация: сортировка в обратном порядке
print("\nСортируем второй массив по 'num_1' в обратном порядке...")
start_time = time.time()
array_2_sorted_reverse = sorted(array_2, key=lambda x: x["num_1"], reverse=True)
sort_time_4 = time.time() - start_time
print(f"Первые 3 элемента, отсортированные по num_1 (обратно): {array_2_sorted_reverse[:3]}")
print(f"Время сортировки в обратном порядке: {sort_time_4:.6f} секунд")

# Статистика
print("\n" + "=" * 50)
print("СТАТИСТИКА:")
print(f"Размер первого массива: {len(array_1)} элементов")
print(f"Размер второго массива: {len(array_2)} элементов")
print(f"Время сортировки пузырьком (100 элементов): {bubble_time:.6f} секунд")
print(f"Время встроенной сортировки (100 000 элементов): {builtin_time:.6f} секунд")
print(
    f"Сортировка пузырьком быстрее встроенного метода в {(builtin_time / bubble_time) * 1000:.0f} раз (на 100 элементах)")
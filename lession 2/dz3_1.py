def factorial(n):
    """
    Вычисляет факториал числа n.
    :param n: Целое число (>= 0).
    :return: Факториал числа n.
    """
    if not isinstance(n, int):
        raise ValueError("Факториал определен только для целых чисел.")
    if n < 0:
        raise ValueError("Факториал определен только для неотрицательных чисел.")

    # Рекурсивная реализация
    def recursive_factorial(x):
        return 1 if x == 0 else x * recursive_factorial(x - 1)

    return recursive_factorial(n)


def find_max(numbers):
    """
    Находит наибольшее число из трёх.
    :param numbers: Кортеж из трёх чисел.
    :return: Наибольшее число.
    """
    if not isinstance(numbers, tuple) or len(numbers) != 3:
        raise ValueError("Аргумент должен быть кортежем из трёх чисел.")
    for num in numbers:
        if not isinstance(num, (int, float)):
            raise ValueError("Все элементы кортежа должны быть числами.")
    return max(numbers)


def triangle_area(a, b):
    """
    Вычисляет площадь прямоугольного треугольника.
    :param a: Длина первого катета.
    :param b: Длина второго катета.
    :return: Площадь треугольника.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise ValueError("Длины катетов должны быть числами.")
    if a <= 0 or b <= 0:
        raise ValueError("Длины катетов должны быть положительными числами.")
    return (a * b) / 2


def get_positive_number(prompt):
    """
    Запрашивает у пользователя положительное число.
    :param prompt: Текст приглашения.
    :return: Положительное число.
    """
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Число должно быть положительным!")
            else:
                return value
        except ValueError:
            print("Ошибка: введите число!")


def get_integer(prompt):
    """
    Запрашивает у пользователя целое число.
    :param prompt: Текст приглашения.
    :return: Целое число.
    """
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Ошибка: введите целое число!")


def main():
    try:
        # 1. Факториал
        print("\n=== Вычисление факториала ===")
        n = get_integer("Введите целое неотрицательное число для вычисления факториала: ")
        print(f"Факториал числа {n}: {factorial(n)}")

        # 2. Поиск наибольшего числа
        print("\n=== Поиск наибольшего числа ===")
        print("Введите три числа:")
        num1 = get_positive_number("Первое число: ")
        num2 = get_positive_number("Второе число: ")
        num3 = get_positive_number("Третье число: ")
        numbers = (num1, num2, num3)
        print(f"Наибольшее число из {numbers}: {find_max(numbers)}")

        # 3. Площадь треугольника
        print("\n=== Расчёт площади прямоугольного треугольника ===")
        a = get_positive_number("Введите длину первого катета: ")
        b = get_positive_number("Введите длину второго катета: ")
        print(f"Площадь треугольника: {triangle_area(a, b)}")

    except ValueError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
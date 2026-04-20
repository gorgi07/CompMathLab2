import contextlib
import io
import math
import os
import sys
from typing import Callable

sys.path.append(os.path.join(os.path.dirname(__file__), "methods"))

from dto.equation import Equation
from methods.chord_method import ChordMethod
from methods.simple_iterations_method import SimpleIterationsMethod
from methods.newton_method import NewtonMethod


ROOT_SCAN_STEPS = 1000
ZERO_EPS = 1e-7


class ExitCommand(Exception):
    pass


def safe_function_call(f: Callable, x: float):
    try:
        value = f(x)

        if isinstance(value, complex):
            return None

        if not math.isfinite(value):
            return None

        return value
    except Exception:
        return None


def read_command(message: str) -> str:
    value = input(message).strip()

    if value.lower() == "exit":
        raise ExitCommand

    return value


def read_int(message: str, min_value: int, max_value: int) -> int:
    while True:
        try:
            value = int(read_command(message))

            if min_value <= value <= max_value:
                return value

            print(f"Введите число от {min_value} до {max_value}.")
        except ValueError:
            print("Некорректный ввод. Введите целое число.")


def read_float(message: str) -> float:
    while True:
        try:
            value = read_command(message).replace(",", ".")
            return float(value)
        except ValueError:
            print("Некорректный ввод. Введите число.")


def read_positive_float(message: str) -> float:
    while True:
        value = read_float(message)

        if value > 0:
            return value

        print("Значение должно быть положительным.")


def analyze_roots(equation: Equation, left: float, right: float):
    f = equation.function

    sign_changes = 0
    zero_points = []

    prev_x = left
    prev_y = safe_function_call(f, prev_x)

    if prev_y is None:
        return False, "Функция не определена в левой границе интервала."

    if abs(prev_y) <= ZERO_EPS:
        zero_points.append(prev_x)

    for i in range(1, ROOT_SCAN_STEPS + 1):
        x = left + (right - left) / ROOT_SCAN_STEPS * i
        y = safe_function_call(f, x)

        if y is None:
            return False, f"Функция не определена на интервале при x = {x:.6f}."

        if abs(y) <= ZERO_EPS:
            if len(zero_points) == 0 or abs(x - zero_points[-1]) > (right - left) / ROOT_SCAN_STEPS * 2:
                zero_points.append(x)

        if prev_y * y < 0:
            sign_changes += 1

        prev_x = x
        prev_y = y

    if sign_changes == 0 and len(zero_points) == 0:
        return False, "На заданном интервале корней не обнаружено."

    if sign_changes > 1 or len(zero_points) > 1:
        return False, "На заданном интервале обнаружено несколько корней. Укажите меньший интервал локализации."

    if not equation.monotonic(left, right):
        return False, "Функция не монотонна на интервале. Нельзя гарантировать единственность корня."

    return True, ""


def print_equations(equations):
    print("\nВыберите уравнение:")

    for number, equation in equations.items():
        print(f"{number}: {equation.text}")


def print_methods(methods):
    print("\nВыберите метод:")

    for number, method_data in methods.items():
        print(f"{number}: {method_data['name']}")


def parse_input_file(file_path: str):
    if not os.path.exists(file_path):
        return None, f"Файл не найден: {file_path}"

    values = {}

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except OSError:
        return None, "Не удалось прочитать файл."

    clear_lines = []

    for line in lines:
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        clear_lines.append(line)

    try:
        if all("=" in line for line in clear_lines):
            for line in clear_lines:
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip().replace(",", ".")
        else:
            if len(clear_lines) < 4:
                return None, "В файле должно быть минимум 4 значения: left, right, epsilon, decimal_places."

            values["left"] = clear_lines[0].replace(",", ".")
            values["right"] = clear_lines[1].replace(",", ".")
            values["epsilon"] = clear_lines[2].replace(",", ".")
            values["decimal_places"] = clear_lines[3].replace(",", ".")

        left = float(values["left"])
        right = float(values["right"])
        epsilon = float(values["epsilon"])
        decimal_places = int(values["decimal_places"])

        if left >= right:
            return None, "Левая граница должна быть меньше правой."

        if epsilon <= 0:
            return None, "Погрешность должна быть положительной."

        if decimal_places < 0 or decimal_places > 15:
            return None, "Количество знаков после запятой должно быть от 0 до 15."

        return {
            "left": left,
            "right": right,
            "epsilon": epsilon,
            "decimal_places": decimal_places,
        }, ""

    except KeyError as error:
        return None, f"В файле отсутствует параметр: {error}."
    except ValueError:
        return None, "В файле есть некорректные числовые данные."


def read_input_data_from_keyboard():
    print("\nВведите исходные данные")

    left = read_float("Левая граница интервала: ")
    right = read_float("Правая граница интервала: ")

    while left >= right:
        print("Левая граница должна быть меньше правой.")
        left = read_float("Левая граница интервала: ")
        right = read_float("Правая граница интервала: ")

    epsilon = read_positive_float("Погрешность вычисления: ")
    decimal_places = read_int("Количество знаков после запятой для вывода: ", 0, 15)

    return {
        "left": left,
        "right": right,
        "epsilon": epsilon,
        "decimal_places": decimal_places,
    }


def read_input_data():
    print("\nВыберите способ ввода исходных данных:")
    print("1: С клавиатуры")
    print("2: Из файла")

    input_type = read_int("Введите номер способа ввода: ", 1, 2)

    if input_type == 1:
        return read_input_data_from_keyboard()

    while True:
        file_path = read_command("Введите путь к файлу с исходными данными: ")
        data, error_message = parse_input_file(file_path)

        if data is not None:
            return data

        print(error_message)


def write_result_to_file(file_path: str, text: str):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text)

        print(f"Результат сохранён в файл: {file_path}")
    except OSError:
        print("Не удалось записать результат в файл.")


def output_result(result_text: str):
    print("\nВыберите способ вывода результата:")
    print("1: На экран")
    print("2: В файл")

    output_type = read_int("Введите номер способа вывода: ", 1, 2)

    if output_type == 1:
        print()
        print(result_text)
        return

    file_path = read_command("Введите путь к файлу для сохранения результата: ")
    write_result_to_file(file_path, result_text)


def solve_task(equations, methods):
    print_equations(equations)
    equation_number = read_int("Введите номер уравнения: ", 1, len(equations))
    equation = equations[equation_number]

    print_methods(methods)
    method_number = read_int("Введите номер метода: ", 1, len(methods))
    method_class = methods[method_number]["class"]

    input_data = read_input_data()

    left = input_data["left"]
    right = input_data["right"]
    epsilon = input_data["epsilon"]
    decimal_places = input_data["decimal_places"]

    print("\nПроверка исходных данных...")

    root_check, root_message = analyze_roots(equation, left, right)
    if not root_check:
        print(root_message)
        return

    method = method_class(equation, left, right, epsilon, decimal_places)

    method_check, method_message = method.check()
    if not method_check:
        print(method_message)
        return

    print("Исходные данные корректны.")
    print("График функции будет построен для всего исследуемого интервала.")

    equation.draw(left, right)

    print("\nВыполнение метода...")

    buffer = io.StringIO()

    with contextlib.redirect_stdout(buffer):
        result = method.solve()

    iterations_log = buffer.getvalue()

    result_text = (
        "Уравнение:\n"
        f"{equation.text}\n\n"
        "Метод:\n"
        f"{methods[method_number]['name']}\n\n"
        "Исходные данные:\n"
        f"Левая граница интервала: {left}\n"
        f"Правая граница интервала: {right}\n"
        f"Погрешность вычисления: {epsilon}\n\n"
        "Итерационный процесс:\n"
        f"{iterations_log}\n"
        f"{result}"
    )

    output_result(result_text)


def main():
    equations = {
        1: Equation(
            lambda x: x ** 3 - x + 4,
            "x^3 - x + 4"
            # https://clck.ru/3TC4Z3
            # x ≈ -1.7963p
        ),
        2: Equation(
            lambda x: -1.38 * x ** 3 - 5.42 * x ** 2 + 2.57 * x + 10.95,
            "-1.38*x^3 - 5.42*x^2 + 2.57*x + 10.95"
            # https://clck.ru/3TC4h7
            # x ≈ -3.88052
            # x ≈ -1.45366
            # x ≈ 1.40664
        ),
        3: Equation(
            lambda x: x ** 3 - 1.89 * x ** 2 - 2 * x + 1.76,
            "x^3 - 1.89*x^2 - 2*x + 1.76"
            # https://clck.ru/3TC4mx
            # x ≈ -1.15624
            # x ≈ 0.629971
            # x ≈ 2.41627
        ),
        4: Equation(
            lambda x: math.sin(x) - x / 2,
            "sin(x) - x/2"
            # https://clck.ru/3TC4q8
            # x ≈ -1.89549
            # x = 0
            # x ≈ 1.89549
        ),
        5: Equation(
            lambda x: math.exp(-x) - x,
            "e^(-x) - x"
            # https://clck.ru/3TC4vk
            # x ≈ 0.56714
        ),
    }

    methods = {
        1: {
            "name": "Метод хорд",
            "class": ChordMethod
        },
        2: {
            "name": "Метод простой итерации",
            "class": SimpleIterationsMethod
        },
        3: {
            "name": "Метод Ньютона",
            "class": NewtonMethod
        },
    }

    print("Программа для численного решения нелинейных уравнений и систем")
    print("Для завершения работы введите exit.")

    while True:
        try:
            solve_task(equations, methods)
        except ExitCommand:
            print("Программа завершена.")
            print("З.Ы. Приходите ещё :)")
            break
        except KeyboardInterrupt:
            print("\nПрограмма завершена.")
            print("З.Ы. Приходите ещё :)")
            break
        except Exception as error:
            print(f"Произошла ошибка: {error}")

        print("\n----------------------------------------")
        print("Новый запуск программы")
        print("Для завершения работы введите exit.")


if __name__ == "__main__":
    main()
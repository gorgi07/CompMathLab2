from dto.result import Result
from method import Method
from utils.derivate import derivate, second_derivate

H = 1e-5
STEPS = 100
MAX_ITERATIONS = 10_000
ZERO_EPS = 1e-12


class NewtonMethod(Method):
    def check(self):
        f = self.equation.function
        a = self.left
        b = self.right

        root_bool = self.equation.root_exists(a, b)
        if not root_bool:
            return False, "На данном интервале корней не существует."

        first_derivative_sign = None
        second_derivative_sign = None

        for i in range(STEPS + 1):
            x = a + (b - a) / STEPS * i

            first_derivative = derivate(f, x, H)
            second_derivative = second_derivate(f, x, H)

            if abs(first_derivative) < ZERO_EPS:
                return False, f"Производная f'(x) близка к нулю при x = {round(x, self.decimal_places)}."

            if abs(second_derivative) < ZERO_EPS:
                continue

            current_first_sign = first_derivative > 0
            current_second_sign = second_derivative > 0

            if first_derivative_sign is None:
                first_derivative_sign = current_first_sign
            elif first_derivative_sign != current_first_sign:
                return False, "Производная f'(x) меняет знак на интервале."

            if second_derivative_sign is None:
                second_derivative_sign = current_second_sign
            elif second_derivative_sign != current_second_sign:
                return False, "Вторая производная f''(x) меняет знак на интервале."

        if not self.__can_choose_start_point():
            return False, "Не удалось выбрать начальное приближение: не выполняется условие f(x0) * f''(x0) > 0."

        return True, ""

    def solve(self):
        f = self.equation.function
        epsilon = self.epsilon
        iteration = 0

        x = self.__choose_start_point()

        while iteration < MAX_ITERATIONS:
            iteration += 1

            first_derivative = derivate(f, x, H)

            if abs(first_derivative) < ZERO_EPS:
                print(f"Производная близка к нулю при x = {round(x, self.decimal_places)}.")

            last_x = x
            x = last_x - f(last_x) / first_derivative

            print(f"{iteration}: x = {round(last_x, self.decimal_places)}, f(x) = {round(f(last_x), self.decimal_places)}, "
                  f"f'(x) = {round(first_derivative, self.decimal_places)}, x_next = {round(x, self.decimal_places)}, "
                  f"|x_k+1 - x_k| = {abs(x - last_x)}")

            if abs(x - last_x) <= epsilon:
                break

            if abs(f(x)) <= epsilon:
                break

            next_first_derivative = derivate(f, x, H)
            if abs(next_first_derivative) >= ZERO_EPS and abs(f(x) / next_first_derivative) <= epsilon:
                break

        return Result(x, f(x), iteration, self.decimal_places)

    def __choose_start_point(self):
        f = self.equation.function
        a = self.left
        b = self.right

        if f(a) * second_derivate(f, a, H) > 0:
            return a

        if f(b) * second_derivate(f, b, H) > 0:
            return b

        return (a + b) / 2

    def __can_choose_start_point(self):
        f = self.equation.function
        a = self.left
        b = self.right

        return f(a) * second_derivate(f, a, H) > 0 or f(b) * second_derivate(f, b, H) > 0

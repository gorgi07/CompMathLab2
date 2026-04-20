from dto.result import Result
from method import Method
from utils.derivate import derivate

H = 1e-5
STEPS = 1000
MAX_ITERATIONS = 10_000


class SimpleIterationsMethod(Method):
    def check(self):
        f = self.equation.function
        a = self.left
        b = self.right

        max_deriv = max(abs(derivate(f, a, H)), abs(derivate(f, b, H)))

        if max_deriv == 0:
            return False, "Производная на границах интервала равна нулю."

        lbd = 1 / max_deriv
        x = (a + b) / 2

        if derivate(f, x, H) > 0:
            lbd *= -1

        def phi(value: float) -> float:
            return value + lbd * f(value)

        for i in range(1, STEPS + 1):
            point = a + (b - a) / STEPS * i

            if abs(derivate(phi, point, H)) >= 1:
                return False, f"Условие сходимости |phi'(x)| < 1 не выполнено при x = {round(point, self.decimal_places)}"

        return True, ""

    def solve(self):
        f = self.equation.function
        a = self.left
        b = self.right
        epsilon = self.epsilon

        x = (a + b) / 2.0
        iteration = 0

        max_deriv = max(abs(derivate(f, a, H)), abs(derivate(f, b, H)))
        lbd = 1 / max_deriv

        if derivate(f, x, H) > 0:
            lbd *= -1

        def phi(value: float) -> float:
            return value + lbd * f(value)

        while iteration < MAX_ITERATIONS:
            iteration += 1

            last_x = x
            x = phi(x)

            print(f"{iteration}: x = {round(x, self.decimal_places)}, f(x) = {round(f(x), self.decimal_places)}, "
                  f"|x_k+1 - x_k| = {abs(x - last_x)}")

            if abs(x - last_x) <= epsilon:
                break

        return Result(x, f(x), iteration, self.decimal_places)

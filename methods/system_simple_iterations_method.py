from dto.system_equation import SystemEquation
from dto.system_result import SystemResult

H = 1e-5
CHECK_STEPS = 20
MAX_ITERATIONS = 10_000


def partial_x1(f, x1: float, x2: float, h: float) -> float:
    return (f(x1 + h, x2) - f(x1 - h, x2)) / (2 * h)


def partial_x2(f, x1: float, x2: float, h: float) -> float:
    return (f(x1, x2 + h) - f(x1, x2 - h)) / (2 * h)


class SystemSimpleIterationsMethod:
    def __init__(self, system: SystemEquation, x1: float, x2: float, epsilon: float, decimal_places: int):
        self.system = system
        self.x1 = x1
        self.x2 = x2
        self.epsilon = epsilon
        self.decimal_places = decimal_places

    def check(self):
        if not self.system.contains_point(self.x1, self.x2):
            return False, "Начальное приближение не принадлежит области проверки сходимости."

        max_q = 0

        for i in range(CHECK_STEPS + 1):
            x1 = self.system.x_left + (self.system.x_right - self.system.x_left) / CHECK_STEPS * i

            for j in range(CHECK_STEPS + 1):
                x2 = self.system.y_left + (self.system.y_right - self.system.y_left) / CHECK_STEPS * j

                row_1 = abs(partial_x1(self.system.phi1, x1, x2, H)) + \
                        abs(partial_x2(self.system.phi1, x1, x2, H))

                row_2 = abs(partial_x1(self.system.phi2, x1, x2, H)) + \
                        abs(partial_x2(self.system.phi2, x1, x2, H))

                q = max(row_1, row_2)
                max_q = max(max_q, q)

                if q >= 1:
                    return False, f"Условие сходимости не выполнено: q = {round(q, self.decimal_places)} при x1 = {round(x1, self.decimal_places)}, x2 = {round(x2, self.decimal_places)}"

        return True, f"Условие сходимости выполнено: q = {round(max_q, self.decimal_places)} < 1"

    def solve(self):
        x1 = self.x1
        x2 = self.x2
        iteration = 0

        error_x1 = 0
        error_x2 = 0

        while iteration < MAX_ITERATIONS:
            iteration += 1

            last_x1 = x1
            last_x2 = x2

            x1 = self.system.phi1(last_x1, last_x2)
            x2 = self.system.phi2(last_x1, last_x2)

            error_x1 = abs(x1 - last_x1)
            error_x2 = abs(x2 - last_x2)

            print(f"{iteration}: "
                  f"x1 = {x1:.6f}, x2 = {x2:.6f}, "
                  f"|x1(k) - x1(k-1)| = {error_x1}, "
                  f"|x2(k) - x2(k-1)| = {error_x2}")

            if max(error_x1, error_x2) <= self.epsilon:
                break

        residual_f1 = self.system.f1(x1, x2)
        residual_f2 = self.system.f2(x1, x2)

        return SystemResult(
            x1,
            x2,
            iteration,
            error_x1,
            error_x2,
            residual_f1,
            residual_f2,
            self.decimal_places
        )
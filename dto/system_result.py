from dataclasses import dataclass


@dataclass
class SystemResult:
    x1: float
    x2: float
    iterations: int
    error_x1: float
    error_x2: float
    residual_f1: float
    residual_f2: float
    decimal_places: int

    def __str__(self):
        return "Результат:\n" \
               f"Вектор неизвестных:\n" \
               f"x1 = {round(self.x1, self.decimal_places)}\n" \
               f"x2 = {round(self.x2, self.decimal_places)}\n\n" \
               f"Количество итераций: {self.iterations}\n\n" \
               f"Вектор погрешностей:\n" \
               f"|x1(k) - x1(k-1)| = {self.error_x1}\n" \
               f"|x2(k) - x2(k-1)| = {self.error_x2}\n\n" \
               f"Проверка решения:\n" \
               f"f1(x1, x2) = {self.residual_f1}\n" \
               f"f2(x1, x2) = {self.residual_f2}"
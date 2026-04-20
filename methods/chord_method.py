from dto.result import Result
from method import Method

MAX_ITERATIONS = 10_000


class ChordMethod(Method):
    def check(self):
        monotonic_bool = self.equation.monotonic(self.left, self.right)
        if not monotonic_bool:
            return False, "Функция не монотонна на интервале: возможно наличие нескольких корней."

        root_bool = self.equation.root_exists(self.left, self.right)
        if not root_bool:
            return False, "На данном интервале корней не существует."

        return True, ""

    def solve(self):
        f = self.equation.function
        a = self.left
        b = self.right
        epsilon = self.epsilon
        iteration = 0

        x = a - (b - a) * f(a) / (f(b) - f(a))
        last_x = x

        while iteration < MAX_ITERATIONS:
            iteration += 1

            if f(a) * f(x) < 0:
                b = x
            else:
                a = x

            x = a - (b - a) * f(a) / (f(b) - f(a))
            print(
                f"{iteration}: a = {round(a, self.decimal_places)}, b = {round(b, self.decimal_places)}, x = {round(x, self.decimal_places)}, "
                f"f(a) = {round(f(a), self.decimal_places)}, f(b) = {round(f(b), self.decimal_places)}, f(x) = {round(f(x), self.decimal_places)}, |x_k+1 - x_k| = {abs(x - last_x)}")

            if abs(f(x)) <= epsilon and abs(x - last_x) <= epsilon:
                break

            last_x = x

        return Result(x, f(x), iteration, self.decimal_places)

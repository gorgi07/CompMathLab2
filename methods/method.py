from dto.equation import Equation


class Method:
    def __init__(self, equation: Equation, left: float, right: float, epsilon: float, decimal_places: int):
        self.equation = equation
        self.left = left
        self.right = right
        self.epsilon = epsilon
        self.decimal_places = decimal_places

    def solve(self):
        pass

    def check(self):
        return True, ""
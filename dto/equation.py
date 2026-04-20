from typing import Callable
import matplotlib.pyplot as plt
import numpy as np


class Equation:
    def __init__(self, function: Callable, text: str):
        self.function = function
        self.text = text

    def draw(self, left: float, right: float) -> None:
        x = np.linspace(left, right)
        func = np.vectorize(self.function)(x)

        plt.title("График функции")
        plt.grid(True, which="both")
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.axhline(y=0, color="gray", label="y = 0")
        plt.plot(x, func, "blue", label=self.text)
        plt.legend(loc="upper left")
        plt.savefig("graph.png")
        plt.show()

    def root_exists(self, left: float, right: float) -> bool:
        return self.function(left) * self.function(right) < 0

    def monotonic(self, left: float, right: float) -> bool:
        steps = 100
        prev = self.function(left)
        step = (right - left) / steps
        is_increasing = self.function(left + step) > prev
        for i in range(1, steps + 1):
            x = left + step * i
            cur = self.function(x)
            if is_increasing and cur < prev:
                return False
            if not is_increasing and cur > prev:
                return False
            prev = cur
        return True

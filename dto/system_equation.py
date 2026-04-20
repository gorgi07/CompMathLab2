from typing import Callable
import matplotlib.pyplot as plt
import numpy as np


class SystemEquation:
    def __init__(
            self,
            f1: Callable,
            f2: Callable,
            phi1: Callable,
            phi2: Callable,
            text: str,
            x_left: float,
            x_right: float,
            y_left: float,
            y_right: float
    ):
        self.f1 = f1
        self.f2 = f2
        self.phi1 = phi1
        self.phi2 = phi2
        self.text = text

        self.x_left = x_left
        self.x_right = x_right
        self.y_left = y_left
        self.y_right = y_right

    def draw(self) -> None:
        x_values = np.linspace(self.x_left, self.x_right, 400)
        y_values = np.linspace(self.y_left, self.y_right, 400)

        x_grid, y_grid = np.meshgrid(x_values, y_values)

        f1_values = np.vectorize(self.f1)(x_grid, y_grid)
        f2_values = np.vectorize(self.f2)(x_grid, y_grid)

        plt.figure()
        plt.title("График системы нелинейных уравнений")
        plt.grid(True, which="both")
        plt.xlabel("x1")
        plt.ylabel("x2")

        plt.contour(x_grid, y_grid, f1_values, levels=[0])
        plt.contour(x_grid, y_grid, f2_values, levels=[0])

        plt.text(
            self.x_left,
            self.y_right,
            "f1(x1, x2) = 0\nf2(x1, x2) = 0",
            verticalalignment="top"
        )

        plt.savefig("system_graph.png")
        plt.show()

    def contains_point(self, x1: float, x2: float) -> bool:
        return self.x_left <= x1 <= self.x_right and self.y_left <= x2 <= self.y_right
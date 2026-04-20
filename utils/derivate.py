def derivate(f, x: float, h: float) -> float:
    return (f(x + h) - f(x - h)) / (2 * h)


def second_derivate(f, x: float, h: float) -> float:
    return (f(x + h) - 2 * f(x) + f(x - h)) / (h ** 2)

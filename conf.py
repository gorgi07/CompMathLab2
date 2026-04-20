equations = {
    1: Equation(
        lambda x: x ** 3 - x + 4,
        "x^3 - x + 4"
        # https://clck.ru/3TC4Z3
        # x ≈ -1.7963
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
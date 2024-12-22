from __future__ import annotations

from collections.abc import Generator

# INPUT = "input_example.txt"
INPUT = "input.txt"

A_TOKENS = 3
B_TOKENS = 1


def read_input() -> Generator[ClawMachine]:
    """
    Read the input file and return a generator of ClawMachine objects

    Example:
        Button A: X+94, Y+34
        Button B: X+22, Y+67
        Prize: X=8400, Y=5400

    Result:
        ClawMachine(a=Point(x=94, y=34), b=Point(x=22, y=67), prize=Point(x=8400, y=5400))
    """
    with open(INPUT) as f:
        for data in f.read().split("\n\n"):
            button_a, button_b, prize = data.strip().split("\n")
            _button, _a, x, y = button_a.split()
            a = Point(int(x[1:-1]), int(y[1:]))
            _button, _b, x, y = button_b.split()
            b = Point(int(x[1:-1]), int(y[1:]))
            _prize, x, y = prize.split()
            p = Point(int(x[2:-1]), int(y[2:]))
            yield ClawMachine(a, b, p)


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"


class ClawMachine:
    def __init__(self, a: Point, b: Point, prize: Point):
        self.a = a
        self.b = b
        self.prize = prize

    def __repr__(self):
        return f"ClawMachine(a={self.a}, b={self.b}, prize={self.prize})"

    def min_tokens(self) -> tuple[float, float]:
        """
        Calculate the minimum number of tokens needed to get the prize
        """
        prize_b = self.prize.x * self.b.y - self.prize.y * self.b.x
        prize_a = self.prize.x * self.a.y - self.prize.y * self.a.x
        a_b = self.a.x * self.b.y - self.a.y * self.b.x
        b_a = self.b.x * self.a.y - self.b.y * self.a.x
        return prize_b / a_b, prize_a / b_a

    def solve(self) -> int | None:
        """
        Solve the claw machine problem
        """
        a_times, b_times = self.min_tokens()

        # Number of presses must be positive
        if a_times < 0 or b_times < 0:
            return 0

        # Number of presses must be integer
        if not a_times.is_integer() or not b_times.is_integer():
            return 0

        # No more than 100 presses per button
        if a_times > 100 or b_times > 100:
            return 0

        return int(a_times * A_TOKENS + b_times * B_TOKENS)


def main():
    tokens = 0
    for machine in read_input():
        tokens += machine.solve()

    print(f"Tokens needed for game: {tokens}")  # 37128


if __name__ == "__main__":
    main()

from collections.abc import Generator

INPUT = "input.txt"
# INPUT = "input_example.txt"


def get_input() -> Generator[tuple[int, list[int]]]:
    """
    Get input from file

    Example:
    190: 10 19
    3267: 81 40 27

    Return:
    (190, [10, 19])
    (3267, [81, 40, 27])
    """
    with open(INPUT) as file:
        for line in file.read().splitlines():
            test_value: int
            numbers: list[int]
            test_value_str, numbers_str = line.split(":")
            test_value = int(test_value_str)
            numbers = list(map(int, numbers_str.split()))
            yield test_value, numbers


def can_solve(test_value: int, result: int, numbers: list[int], calibrate=False):
    """
    Solve equations using addition (`+`) and multiplication (`*`).

    :param: calibrate: If True, it will allow to concatenate numbers. Default is False.

    Example:
    190: 10 19
    3267: 81 40 27
    7290: 6 8 6 15  # calibrate=True

    Result:
    190 = 10 * 19
    3267 = 81 * 40 + 27 (or 81 + 40 * 27)
    7290 = 6 * 8 || 6 * 15
    """
    if result > test_value:
        return False

    if not numbers:
        return test_value == result

    number = numbers.pop(0)
    return any(
        [
            can_solve(test_value, result + number, numbers.copy(), calibrate),
            can_solve(test_value, result * number, numbers.copy(), calibrate),
            (
                can_solve(
                    test_value, int(f"{result}{number}"), numbers.copy(), calibrate
                )
                if calibrate
                else False
            ),
        ]
    )


def main():
    test_values = 0
    for test_value, numbers in get_input():
        if can_solve(test_value, 0, numbers):
            test_values += test_value
    print(f"Sum of test values: {test_values}")  # 2664460013123
    test_values_with_calibration = 0
    for test_value, numbers in get_input():
        if can_solve(test_value, 0, numbers, calibrate=True):
            test_values_with_calibration += test_value
    print(
        f"Sum of test values with calibration: {test_values_with_calibration}"
    )  # 426214131924213


if __name__ == "__main__":
    main()

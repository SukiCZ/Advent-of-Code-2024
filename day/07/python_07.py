INPUT = "input.txt"
# INPUT = "input_small.txt"


def get_input() -> tuple[int, list[int]]:
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
            test_value, numbers = line.split(":")
            test_value = int(test_value)
            numbers = list(map(int, numbers.split()))
            yield test_value, numbers


def can_solve(test_value, result, numbers):
    """
    Solve equations using addition (`+`) and multiplication (`*`).

    Example:
    190: 10 19
    3267: 81 40 27

    Result:
    190 = 10 * 19
    3267 = 81 * 40 + 27 (or 81 + 40 * 27)
    """
    if result > test_value:
        return False

    if not numbers:
        return test_value == result

    number = numbers.pop(0)
    return any(
        [
            can_solve(test_value, result + number, numbers.copy()),
            can_solve(test_value, result * number, numbers.copy()),
        ]
    )


def main():
    test_values = 0
    for test_value, numbers in get_input():
        if can_solve(test_value, 0, numbers):
            test_values += test_value
    print(f"Sum of test values: {test_values}")  # 2664460013123


if __name__ == "__main__":
    main()

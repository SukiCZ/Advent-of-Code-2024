import re


INPUT_FILE = "input.txt"
REGEX = re.compile(
    r"mul\((?P<left>[0-9]{1,3}),(?P<right>[0-9]{1,3})\)"
)  # mul(123,456) -> left=123, right=456


def read_lines():
    with open(INPUT_FILE, "r") as file:
        for line in file:
            yield line


def sum_line(line):
    result = 0
    for mul in REGEX.finditer(line):
        # Extract left and right values from the "mul" call
        # e.g. mul(123,456) -> 123 * 456
        left, right = map(int, mul.groups())
        result += left * right
    return result


def sum_multiplication_calls(lines):
    # Summarise result of "multiplication" calls
    return sum(sum_line(line) for line in lines)


def part_two(lines):
    # Same as sum_multiplication_calls() but keywords `do()` amd `don't()` turn on/off the multiplication
    result = 0
    # Join lines into one string
    line = "".join(lines)
    # Split the string by "do()"
    do_lines = line.split("do()")
    for do_line in do_lines:
        # Split the string by "don't()"
        do, *_dont = do_line.split("don't()")
        # Find all "mul" calls in the "do()" part
        result += sum_line(do)
    return result


if __name__ == "__main__":
    lines = list(read_lines())
    mul_calls = sum_multiplication_calls(lines)
    print(f"Sum of 'mul' calls: {mul_calls}")  # 164730528
    mul_calls_with_do_dont = part_two(lines)
    print(
        f"Sum of 'mul' calls with 'do()' and 'don't()': {mul_calls_with_do_dont}"
    )  # 70478672

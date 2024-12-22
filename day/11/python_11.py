from functools import cache

# INPUT = "input_example.txt"
INPUT = "input.txt"

MULTIPLY_BY = 2024


def read_input() -> list[int]:
    """
    Read input file and return list of integers, graved into the stones
    """
    with open(INPUT) as file:
        return [int(char) for char in file.readline().split()]


@cache
def transform_stone(stone: int) -> list[int]:
    """
    Transformation rules:

    If stone is zero, it will be transformed to one (`0` -> `1`)
    If stone has even numbers of digits, split in two (`1000` -> (`10`, `0`))
    Otherwise multiply by 2024 (`100` -> `202400`)
    """
    if stone == 0:
        return [1]
    if len(str(stone)) % 2 == 0:
        s = str(stone)  # Convert to string
        idx_half = len(str(stone)) // 2  # Get half index
        first, second = s[:idx_half], s[idx_half:]  # Split in two
        return [int(first), int(second)]  # Convert back to integer
    return [stone * MULTIPLY_BY]


def transform(data: list[int]) -> list[int]:
    """
    For each stone, check transformation rules
    """
    result: list[int] = []
    for stone in data:
        result.extend(transform_stone(stone))
    return result


def main():
    data = read_input()
    for _ in range(25):
        data = transform(data)
    print(f"Number of stones after 25 transformations: {len(data)}")


if __name__ == "__main__":
    main()

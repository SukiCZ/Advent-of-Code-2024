from collections import Counter

# INPUT = "input_example.txt"
INPUT = "input.txt"

MULTIPLY_BY = 2024


def read_input() -> list[int]:
    """
    Read input file and return list of integers, graved into the stones
    """
    with open(INPUT) as file:
        return [int(char) for char in file.readline().split()]


def transform_stones(counter: Counter) -> Counter:
    """
    Transformation rules:

    If stone is zero, it will be transformed to one (`0` -> `1`)
    If stone has even numbers of digits, split in two (`1000` -> (`10`, `0`))
    Otherwise multiply by 2024 (`100` -> `202400`)
    """
    new_counter: Counter[int] = Counter()

    for stone, count in counter.items():
        if stone == 0:
            new_counter[1] += count
        elif len(str(stone)) % 2 == 0:
            s = str(stone)  # Convert to string
            idx_half = len(str(stone)) // 2  # Get half index
            first, second = s[:idx_half], s[idx_half:]  # Split in two
            new_counter[int(first)] += count
            new_counter[int(second)] += count
        else:
            new_counter[stone * MULTIPLY_BY] += count

    return new_counter


def transform(data: list[int], iterations: int) -> Counter:
    """
    For each stone, check transformation rules
    """
    counter: Counter[int] = Counter(data)
    for _ in range(iterations):
        counter = transform_stones(counter)
    return counter


def main():
    data = read_input()
    stone_counts = transform(data, 25)
    print(f"Number of stones after 25 transformations: {sum(stone_counts.values())}")  # 193269


if __name__ == "__main__":
    main()

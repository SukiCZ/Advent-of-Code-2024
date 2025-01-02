from functools import cache

INPUT = "input.txt"


def read_input() -> tuple[set[str], list[str]]:
    with open(INPUT) as f:
        _towels, _patterns = f.read().split("\n\n")
        towels = set(_towels.split(", "))
        patterns = _patterns.strip().split("\n")
        return towels, patterns


def can_form_pattern(towels: set[str], pattern: str) -> bool:
    """
    Recursive function to check if a pattern can be formed by the towels.
    :param towels: Towels to use to form a pattern.
    :param pattern: Pattern to form.
    :return: True if the pattern can be formed, False otherwise.
    """
    for towel in towels:
        # If the towel is the pattern, return True.
        if towel == pattern:
            return True
        # If the pattern starts with the towel, check if the rest of the pattern can be formed.
        if pattern.startswith(towel):
            if can_form_pattern(towels, pattern[len(towel) :]):
                return True
    # If the pattern cannot be formed, return False.
    return False


def count_formations(towels: set[str], patterns: list[str]) -> int:
    """
    Recursive function to count the number of formations of a pattern.
    :param towels: Towels to use to form a pattern.
    :param patterns: Patterns to form.
    :return: Number of formations of the pattern.
    """

    @cache
    def count_formation(pattern: str) -> int:
        count = 0
        for towel in towels:
            # If the towel is the pattern, increment the count.
            if towel == pattern:
                count += 1
            # If the pattern starts with the towel, count the number of formations of the rest of the pattern.
            if pattern.startswith(towel):
                count += count_formation(pattern[len(towel) :])
        return count

    return sum([count_formation(pattern) for pattern in patterns])


def main():
    towels, patterns = read_input()
    count_can_form = sum([can_form_pattern(towels, pattern) for pattern in patterns])
    count_formation = count_formations(towels, patterns)
    print(f"{count_can_form} patterns can be formed by the towels.")
    print(f"{count_formation} formations of the patterns can be made by the towels.")


if __name__ == "__main__":
    main()

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


def main():
    towels, patterns = read_input()
    count = sum([can_form_pattern(towels, pattern) for pattern in patterns])
    print(f"{count} patterns can be formed by the towels.")


if __name__ == "__main__":
    main()

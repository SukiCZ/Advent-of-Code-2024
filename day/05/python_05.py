from collections import defaultdict

INPUT = "input.txt"


def get_middle(lst: list[int]) -> int:
    return lst[len(lst) // 2]


def read_input(file):
    """
    Input file example:
    1|3
    3|5

    1,3,5
    :param file:
    :return: tuple of to_right, to_left and updates
    to_right: {1: [3], 3: [5], 5: []}
    to_left: {3: [1], 5: [3]}
    updates: [[1, 3, 5]]
    """
    updates = []
    to_left = defaultdict(list)
    to_right = defaultdict(list)
    with open(file) as f:
        while line := f.readline().strip():  # Walrus operator (Assignment expressions)
            l, r = line.split("|")
            l, r = int(l), int(r)
            to_right[l].append(r)
            to_left[r].append(l)

        for line in f:
            updates.append(list(map(int, line.strip().split(","))))

    return to_right, to_left, updates


def validate_updates(
    update: list[int], to_right: dict[int, list[int]], to_left: dict[int, list[int]]
) -> int | None:
    """
    Checks update in order to_right and to_left
    :param update: [1, 3, 5]
    :param to_right: {1: [3, 5], 3: [5], 5: []}
    :param to_left: {3: [1], 5: [1, 3]}
    :return: 3 (middle element of valid update) or None (invalid update)
    """
    left: list[int] = []
    right = update
    while right:
        i = right.pop(0)
        for j in right:
            if j in to_left[i]:
                return None
        for j in left:
            if j in to_right[i]:
                return None
        left.append(i)
    return get_middle(left)


def fix_update(
    update: list[int], to_right: dict[int, list[int]], to_left: dict[int, list[int]]
) -> int:
    """
    Fix update in order to_right and to_left
    :param update: [3, 1, 5]
    :param to_right: {1: [3, 5], 3: [5], 5: []}
    :param to_left: {3: [1], 5: [1, 3]}
    :return: 3 (middle element of valid update) or None (invalid update)
    """
    left = []
    right = update
    while right:
        i = right.pop(0)
        for idx, j in enumerate(right):
            if j in to_left[i]:
                left.append(i)
                break
        else:
            for idx, j in enumerate(left):
                if j in to_right[i]:
                    left.insert(idx, i)
                    break
            else:
                left.append(i)
    return get_middle(left)


if __name__ == "__main__":
    to_right, to_left, updates = read_input(INPUT)
    result = 0
    result_2 = 0
    for update in updates:
        middle = validate_updates(update.copy(), to_right, to_left)
        if middle is not None:
            result += middle
        else:
            result_2 += fix_update(update.copy(), to_right, to_left)
    print(f"Result: {result}")  # 6498
    print(f"Result part 2: {result_2}")  # 5017

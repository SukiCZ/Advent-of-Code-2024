from collections import defaultdict


INPUT_FILE = "input.txt"


def read_lists() -> (list, list):
    with open(INPUT_FILE, "r") as file:
        list_1, list_2 = [], []
        # Read file to list variables
        for line in file:
            one, two = line.split()
            list_1.append(int(one))
            list_2.append(int(two))
        return list_1, list_2


def main():
    result = 0
    # Read file to list variables
    list_1, list_2 = read_lists()
    # Sort the lists
    list_1.sort()
    list_2.sort()
    # Calculate the result
    for one, two in zip(list_1, list_2):
        result += abs(one - two)
    print(f"The result is: {result}")  # 2176849


def part_two():
    result = 0
    location_counter = defaultdict(int)
    # Read file to list variables
    list_1, list_2 = read_lists()
    # Count the number of times a value appears in the list_2
    for value in list_2:
        location_counter[value] += 1
    # Calculate the result
    for value in list_1:
        result += value * location_counter[value]
    print(f"The part two result is: {result}")  # 23384288


if __name__ == "__main__":
    main()
    part_two()

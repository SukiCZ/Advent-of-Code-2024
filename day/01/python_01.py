from collections import defaultdict


def read_lists(input_file: str) -> (list, list):
    with open(input_file, "r") as file:
        list_1, list_2 = [], []
        # Read file to list variables
        for line in file:
            one, two = line.split()
            list_1.append(int(one))
            list_2.append(int(two))
        return list_1, list_2


def main(input_file: str):
    result = 0
    # Read file to list variables
    list_1, list_2 = read_lists(input_file)
    # Sort the lists
    list_1.sort()
    list_2.sort()
    # Calculate the result
    for one, two in zip(list_1, list_2):
        result += abs(one - two)
    print(f"The result is: {result}")


def part_two(input_file: str):
    result = 0
    location_counter = defaultdict(int)
    # Read file to list variables
    list_1, list_2 = read_lists(input_file)
    # Count the number of times a value appears in the list_2
    for value in list_2:
        location_counter[value] += 1
    # Calculate the result
    for value in list_1:
        result += value * location_counter[value]
    print(f"The part two result is: {result}")


if __name__ == "__main__":
    input_file = "../input.txt"
    main(input_file)
    part_two(input_file)

INPUT_FILE = "input.txt"


def get_line():
    with open(INPUT_FILE, "r") as file:
        for line in file:
            yield line


def is_increasing_or_decreasing(reports: [int]) -> bool:
    # Check if the reports are increasing or decreasing
    direction = None
    for i in range(1, len(reports)):
        # Check if the difference between the reports is between 1 and 3
        diff = reports[i] - reports[i - 1]
        if not (1 <= abs(diff) <= 3):
            return False
        # Check if the reports are increasing or decreasing
        if direction is None:
            direction = diff
        # If the direction is different from the previous direction
        elif (direction > 0 > diff) or (direction < 0 < diff):
            return False

    return True

def part_one():
    safe_reports = 0
    for line in get_line():
        reports = [int(report) for report in line.split()]
        if is_increasing_or_decreasing(reports):
            safe_reports += 1

    print(f"Safe reports: {safe_reports}")  # 534


if __name__ == "__main__":
    part_one()

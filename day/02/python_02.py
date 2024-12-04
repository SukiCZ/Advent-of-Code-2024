INPUT_FILE = "input.txt"


def read_lines():
    with open(INPUT_FILE, "r") as file:
        for line in file:
            yield line


def is_increasing_or_decreasing(reports: [int], allowed_fails: int = 0) -> bool:
    # Check if the reports are increasing or decreasing
    direction = None
    fails = 0
    for i in range(1, len(reports)):
        # Check if the difference between the reports is between 1 and 3
        diff = reports[i] - reports[i - 1]
        if not (1 <= abs(diff) <= 3):
            fails += 1
            if fails > allowed_fails:
                return False
            continue
        # Check if the reports are increasing or decreasing
        if direction is None:
            direction = diff
        # If the direction is different from the previous direction
        elif (direction > 0 > diff) or (direction < 0 < diff):
            fails += 1
            if fails > allowed_fails:
                return False
    return True


def main():
    lines = [[int(i) for i in line.split()] for line in read_lines()]
    safe_reports = sum(is_increasing_or_decreasing(reports) for reports in lines)
    safe_reports_with_one_fail = sum(
        is_increasing_or_decreasing(reports, allowed_fails=1) for reports in lines
    )

    print(f"Safe reports: {safe_reports}")  # 534
    print(f"Safe reports with allowed fail: {safe_reports_with_one_fail}")  # 577


if __name__ == "__main__":
    main()

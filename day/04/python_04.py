INPUT_FILE = "input.txt"  # Path to the input file
WORD = "XMAS"  # Word to search in the grid
# Define the 8 possible directions (dx, dy)
DIRECTIONS = [
    (0, 1),  # right
    (1, 0),  # down
    (0, -1),  # left
    (-1, 0),  # up
    (1, 1),  # down-right
    (1, -1),  # down-left
    (-1, 1),  # up-right
    (-1, -1),  # up-left
]
PATTERN = "MAS"
PATTERN_LEN = len(PATTERN)
PATTERNS = [
    [("M", -1, -1), ("S", -1, 1), ("A", 0, 0), ("M", 1, -1), ("S", 1, 1)],  # Original
    [("S", -1, -1), ("M", 1, -1), ("A", 0, 0), ("S", -1, 1), ("M", 1, 1)],  # + 90
    [("S", 1, -1), ("M", 1, 1), ("A", 0, 0), ("S", -1, -1), ("M", -1, 1)],  # + 180
    [("M", -1, 1), ("S", 1, 1), ("A", 0, 0), ("M", -1, -1), ("S", 1, -1)],  # + 270
]


def read_grid(file_path) -> list[str]:
    # Read the grid from the file
    with open(file_path) as file:
        return [line.strip() for line in file]


def is_valid(x, y, n, m) -> bool:
    # Check if the cell (x, y) is inside the grid
    return 0 <= x < n and 0 <= y < m


def search_word(grid, word):
    # Search for the word in the grid
    n, m = len(grid), len(grid[0])
    word_len = len(word)
    count = 0

    # Iterate over the grid
    for i in range(n):
        # Iterate over the columns
        for j in range(m):
            # Iterate over the directions
            for dx, dy in DIRECTIONS:
                x, y = i, j
                k = 0
                # Check if the word is in the grid
                while k < word_len and is_valid(x, y, n, m) and grid[x][y] == word[k]:
                    x += dx
                    y += dy
                    k += 1
                # If the word is found, increment the count
                if k == word_len:
                    count += 1

    return count


def search_pattern(grid, i, j, pattern):
    # Search for the pattern in the grid
    n, m = len(grid), len(grid[0])
    for char, dx, dy in pattern:
        new_i, new_j = i + dx, j + dy
        if not is_valid(new_i, new_j, n, m) or grid[new_i][new_j] != char:
            return False
    return True


def search_x_mas(grid):
    # Search for the X-MAS pattern in the grid
    n, m = len(grid), len(grid[0])
    count = 0

    for i in range(n):
        for j in range(m):
            for pattern in PATTERNS:
                if search_pattern(grid, i, j, pattern):
                    count += 1

    return count


if __name__ == "__main__":
    grid = read_grid(INPUT_FILE)
    occurrences = search_word(grid, WORD)
    print(f"The word '{WORD}' appears {occurrences} times in the grid.")  # 2454
    occurrences = search_x_mas(grid)
    print(f"The X-MAS pattern appears {occurrences} times in the grid.")  # 1858

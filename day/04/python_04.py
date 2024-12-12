INPUT_FILE = "input.txt"  # Path to the input file
WORD = "XMAS"
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


def read_grid(file_path) -> list[str]:
    # Read the grid from the file
    with open(file_path, "r") as file:
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


if __name__ == "__main__":
    grid = read_grid(INPUT_FILE)
    occurrences = search_word(grid, WORD)
    print(f"The word '{WORD}' appears {occurrences} times in the grid.")  # 2454

# INPUT = "input_example.txt"
INPUT = "input.txt"

DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def read_input() -> list[list[int]]:
    with open(INPUT) as f:
        return [[int(c) for c in line] for line in f.read().splitlines()]


class Grid:
    def __init__(self, grid: list[list[int]]):
        self.height = len(grid)
        self.width = len(grid[0])
        self.grid = grid

    def __str__(self):
        return "\n".join("".join(str(c) for c in line) for line in self.grid)

    def on_map(self, x: int, y: int) -> bool:
        """
        Check if x, y is on the map
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def get_trailheads_start(self) -> list[tuple[int, int]]:
        """
        Return location of 0s in the grid
        """
        return [(x, y) for y in range(self.height) for x in range(self.width) if self.grid[y][x] == 0]

    def get_neighbors(self, x, y, visited) -> list[tuple[int, int]]:
        """
        Get neighbors of a cell that applies
        """
        return [
            (x + dx, y + dy)
            for dx, dy in DIRECTIONS
            if self.on_map(x + dx, y + dy)  # On the map
            and self.grid[y + dy][x + dx] == self.grid[y][x] + 1  # Next cell > current by 1
            and not visited[y + dy][x + dx]  # Not visited
        ]

    def analyze_path(self, x, y, visited=None) -> int:
        """
        Analyze the path starting at x, y
        """
        if visited is None:
            visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        current = self.grid[y][x]
        visited[y][x] = True
        if current == 9:
            return 1

        return sum(
            self.analyze_path(dx, dy, visited=visited) for dx, dy in self.get_neighbors(x, y, visited=visited)
        )


def main():
    score = 0
    data = read_input()
    grid = Grid(data)
    for x, y in grid.get_trailheads_start():
        score += grid.analyze_path(x, y)
    print(f"Summary of path score is: {score}")  # 646


if __name__ == "__main__":
    main()

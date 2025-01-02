import heapq
from collections import defaultdict
from dataclasses import dataclass

INPUT = "input.txt"
WIDTH = 70
HEIGHT = 70
N_STEPS = 1024

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up


def float_inf() -> float:
    return float("inf")


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)


def read_input() -> list[Point]:
    """
    Read the input file and return a list of points

    Example:
    5,4
    4,2
    4,5

    Returns:
    [Point(5, 4), Point(4, 2), Point(4, 5)]

    :return: List of points
    """
    with open(INPUT) as f:
        return [Point(y=int(line.split(",")[0]), x=int(line.split(",")[1])) for line in f.readlines()]


class Maze:
    def __init__(self, memory_space: list[Point]):
        """
        Initialize the maze with the memory space

        :param memory_space: List of points where bytes fall into
        """
        self.memory_space = memory_space
        self.width = WIDTH
        self.height = HEIGHT
        self.start = Point(0, 0)
        self.end = Point(self.width, self.height)
        self.visited: dict[Point, float] = defaultdict(float_inf)  # (position, direction) -> cost
        self.visited[self.start] = 0

    def on_map(self, position: Point) -> bool:
        """
        Check if the position is on the map
        :param position: Position ot check
        :return: True if the position is on the map
        """
        return 0 <= position.x < self.height + 1 and 0 <= position.y < self.width + 1

    def is_valid(self, position: Point) -> bool:
        """
        Check if the position is valid, meaning it is on the map and not in the memory space
        :param position: Position to check
        :return: True if the position is valid
        """
        return self.on_map(position) and position not in self.memory_space

    def dijkstra(self) -> int | None:
        """
        Dijkstra's algorithm
        https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
        :return:
        """

        # Priority queue with the cost
        pq = [(0, self.start)]

        while pq:
            cost, position = heapq.heappop(pq)

            # Skip visited with lower cost
            if self.visited[position] < cost:
                continue

            # Move into all directions
            for dy, dx in DIRECTIONS:
                new_position = position + Point(x=dx, y=dy)
                if self.is_valid(new_position):
                    new_cost = cost + 1
                    if self.visited[new_position] > new_cost:
                        self.visited[new_position] = new_cost
                        heapq.heappush(pq, (new_cost, new_position))

        return int(self.visited[self.end])

    def print(self):
        """
        Print the maze for debugging purposes
        """
        for i in range(self.height + 1):
            for j in range(self.width + 1):
                point = Point(i, j)
                if point in self.memory_space:
                    print("#", end="")
                elif point in self.visited:
                    print("O", end="")
                else:
                    print(".", end="")
            print()


def main():
    memory_space = read_input()
    maze = Maze(memory_space[:N_STEPS])
    maze.print()
    steps = maze.dijkstra()
    print(f"Steps to exit the maze: {steps}")


if __name__ == "__main__":
    main()

import heapq
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import product

INPUT = "input.txt"

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left


def read_input() -> list[str]:
    with open(INPUT) as f:
        return f.read().splitlines()


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


class Maze:
    def __init__(self, data: list[str]):
        self.data = data
        self.height = len(data)
        self.width = len(data[0])
        for i in range(self.height):
            for j in range(self.width):
                if data[i][j] == "S":
                    self.start = Point(i, j)
                elif data[i][j] == "E":
                    self.end = Point(i, j)
        self.visited: dict[Point, float | int] = defaultdict(float_inf)  # position: cost
        self.visited[self.start] = 0

    def on_map(self, position: Point) -> bool:
        return 0 <= position.x < self.height and 0 <= position.y < self.width

    def is_valid(self, position: Point) -> bool:
        return self.on_map(position) and self.data[position.x][position.y] != "#"

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

            # Move to any direction
            for dx, dy in DIRECTIONS:
                new_position = position + Point(dx, dy)
                if self.is_valid(new_position):
                    new_cost = cost + 1  # cost of move
                    if self.visited[new_position] > new_cost:
                        self.visited[new_position] = new_cost
                        heapq.heappush(pq, (new_cost, new_position))

        if not self.visited[self.end].is_integer():
            return None
        else:
            return int(self.visited[self.end])

    def find_cheating_paths(self, threshold: int, radius: int = 2) -> int:
        """
        Find all cheating paths

        :param threshold: The threshold for the difference between the max and min neighbor
        :param radius: The radius of a cheat to check
        """
        counter: Counter[int] = Counter()

        for x in range(1, self.height - 1):
            for y in range(1, self.width - 1):

                # Check if the point is a wall
                if self.data[x][y] != "#":
                    point = Point(x, y)
                    # For radius in all directions
                    for dx, dy in product(range(-radius, radius + 1), repeat=2):
                        # Skip the point itself
                        if (dx, dy) == (0, 0):
                            continue
                        # Calculate the steps to the neighbor
                        steps = abs(dx) + abs(dy)
                        # Skip if the steps are greater than the radius
                        if steps > radius:
                            continue
                        # Check if the neighbor is visited
                        new_point = point + Point(dx, dy)
                        if self.visited[new_point].is_integer():
                            # Calculate the difference between the max and min neighbor
                            diff = self.visited[new_point] - self.visited[point] - steps
                            if diff >= threshold:
                                counter[int(diff)] += 1

        return sum(counter.values())

    def print(self):
        """
        Print the maze for debugging purposes
        """
        for i in range(self.height):
            for j in range(self.width):
                point = Point(i, j)
                if self.data[i][j] == "#":
                    print("#", end="")
                elif point in self.visited:
                    print("O", end="")
                else:
                    print(".", end="")
            print()


def main():
    data = read_input()
    maze = Maze(data)
    maze.dijkstra()
    # maze.print()
    cheats = maze.find_cheating_paths(threshold=100)
    print(f"Cheating paths: {cheats} with threshold 100 and radius 2")
    cheats = maze.find_cheating_paths(threshold=100, radius=20)
    print(f"Cheating paths: {cheats} with threshold 100 and radius 20")


if __name__ == "__main__":
    main()

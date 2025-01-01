import heapq
from collections import defaultdict
from dataclasses import dataclass

INPUT = "input.txt"
# INPUT = "input_example.txt"  # 11048
# INPUT = "input_example_small.txt"  # 7036

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up


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
        self.direction = 0  # right
        self.visited: dict[tuple[Point, int], float] = defaultdict(float_inf)  # (position, direction) -> cost

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
        pq = [(0, (self.start, self.direction))]

        while pq:
            cost, (position, direction) = heapq.heappop(pq)

            # Skip visited with lower cost
            if self.visited[(position, direction)] < cost:
                continue

            # Move forward
            dx, dy = DIRECTIONS[direction]
            new_position = position + Point(dx, dy)
            if self.is_valid(new_position):
                new_cost = cost + 1  # cost of moving forward
                if self.visited[(new_position, direction)] > new_cost:
                    self.visited[(new_position, direction)] = new_cost
                    heapq.heappush(pq, (new_cost, (new_position, direction)))

            # Rotate left and right
            for new_direction in [(direction + 1) % 4, (direction - 1) % 4]:
                new_cost = cost + 1000  # cost of rotation
                if self.visited[(position, new_direction)] > new_cost:
                    self.visited[(position, new_direction)] = new_cost
                    heapq.heappush(pq, (new_cost, (position, new_direction)))

        return int(min(self.visited[(self.end, direction)] for direction in range(4)))


def main():
    data = read_input()
    maze = Maze(data)
    # print(maze.data)
    print(f"Solution to part 1: {maze.dijkstra()}")  # 65436


if __name__ == "__main__":
    main()

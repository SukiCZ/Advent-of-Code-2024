import heapq
from collections import defaultdict, deque
from dataclasses import dataclass

INPUT = "input.txt"  # 65436, 489
# INPUT = "input_example.txt"  # 11048, 64
# INPUT = "input_example_small.txt"  # 7036, 45

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
        self.direction = 0  # right
        self.visited: dict[tuple[Point, int], float] = defaultdict(float_inf)  # (position, direction) -> cost
        self.visited[(self.start, self.direction)] = 0

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

    def backtrack(self, min_cost: int) -> int:
        """
        Backtrack the shortest path
        :param min_cost: Cost of the shortest path
        :return: Count of unique tiles in the shortest path
        """
        shortest_path: set[tuple[Point, int]] = set()  # set of shortest path tiles
        q: deque[tuple[Point, int]] = deque()  # queue for backtracking

        for d in range(4):
            # Add all end state with the minimum cost
            if self.visited[(self.end, d)] == min_cost:
                shortest_path.add((self.end, d))
                q.append((self.end, d))

        while q:
            position, direction = q.popleft()
            current_cost = self.visited[(position, direction)]

            # Backtrack moves
            dx, dy = DIRECTIONS[direction]
            new_position = position - Point(dx, dy)
            if self.is_valid(new_position):
                new_state = (new_position, direction)
                if 0 <= current_cost - 1 == self.visited[new_state]:
                    if new_state not in shortest_path:
                        shortest_path.add(new_state)
                        q.append(new_state)

            # Backtrack rotations
            if current_cost >= 1000:
                for new_direction in [(direction + 1) % 4, (direction - 1) % 4]:
                    new_state = (position, new_direction)
                    if self.visited[new_state] == current_cost - 1000:
                        if new_state not in shortest_path:
                            shortest_path.add(new_state)
                            q.append(new_state)

        return len({p for (p, d) in shortest_path})


def main():
    data = read_input()
    maze = Maze(data)
    # print(maze.data)
    min_cost = maze.dijkstra()
    print(f"Shortest path cost: {min_cost}")  # 65436
    print(f"Unique tiles in the shortest path: {maze.backtrack(min_cost)}")  # 489


if __name__ == "__main__":
    main()

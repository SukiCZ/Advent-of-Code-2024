INPUT = "input.txt"

UP = "^"
RIGHT = ">"
DOWN = "v"
LEFT = "<"
OBSTACLE = "#"
VISITED = "X"
NOTHING = "."

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
DIRECTIONS_STR = [UP, RIGHT, DOWN, LEFT]


class Guard:
    """
    Guard class represents the guard in the world.
    """

    def __init__(self, x: int, y: int):
        """
        Constructor for the Guard class.
        :param x: X coordinate
        :param y: Y coordinate
        """
        self.x = x
        self.y = y
        self.direction = 0

    def move(self):
        """
        Move the guard in the direction it is facing.
        """
        x, y = DIRECTIONS[self.direction]
        self.x += x
        self.y += y

    def turn(self):
        """
        Turn the guard 90° to the right.
        """
        self.direction = (self.direction + 1) % 4

    def position_ahead(self) -> tuple[int, int]:
        """
        Get the position ahead of the guard.
        """
        x, y = DIRECTIONS[self.direction]
        return self.x + x, self.y + y

    def __str__(self):
        """
        String representation of the guard and its direction.
        """
        return DIRECTIONS_STR[self.direction]


class Obstacle:
    """
    Obstacle class represents an obstacle in the world.
    """

    def __init__(self, x, y):
        """
        Constructor for the Obstacle class.
        :param x: X coordinate
        :param y: Y coordinate
        """
        self.x = x
        self.y = y

    def __str__(self):
        """
        String representation of the obstacle.
        """
        return OBSTACLE


class World:
    """
    World-class represents the world the guard is walking in.
    """

    def __init__(self, data: list[str]):
        """
        Constructor for the World class.
        :param data: List of strings representing the world.
        """
        self.height: int = len(data)
        self.width: int = len(data[0])
        self.guard: Guard | None = None
        self.obstacles: set = set()
        self.visited: set = set()

        for i in range(self.height):
            for j in range(self.width):
                if data[i][j] == UP:
                    self.guard = Guard(i, j)
                elif data[i][j] == OBSTACLE:
                    self.obstacles.add(Obstacle(i, j))

    def walk(self):
        """
        Walk the guard in the world.
        """
        x, y = self.guard.position_ahead()

        if any([o.x == x and o.y == y for o in self.obstacles]):
            self.guard.turn()
            return

        visit = (self.guard.x, self.guard.y)
        if visit not in self.visited:
            self.visited.add(visit)
        self.guard.move()

    def on_map(self, x, y) -> bool:
        """
        Check if the given coordinates are on the map.
        """
        return 0 <= x < self.height and 0 <= y < self.width

    def print(self):
        """
        Print the world.
        """
        for i in range(self.height):
            for j in range(self.width):
                if self.guard.x == i and self.guard.y == j:
                    print(self.guard, end="")
                elif any([o.x == i and o.y == j for o in self.obstacles]):
                    print(OBSTACLE, end="")
                elif (i, j) in self.visited:
                    print(VISITED, end="")
                else:
                    print(NOTHING, end="")
            print("")
        print("\n\n\n")

    def print_stats(self):
        """
        Print the statistics of the world.
        """
        print(
            {
                "height": self.height,
                "width": self.width,
                "visited": len(self.visited),
                "obstacles": len(self.obstacles),
            }
        )


def main():
    with open(INPUT, "r") as f:
        data = f.read().splitlines()

    world = World(data)
    while True:
        world.walk()
        if not world.on_map(world.guard.x, world.guard.y):
            break

    world.print_stats()  # visited: 4647, obstacles: 807
    world.print()


if __name__ == "__main__":
    main()

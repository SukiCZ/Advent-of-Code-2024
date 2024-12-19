INPUT = "input.txt"
# INPUT = "input_small.txt"

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
        self.start: tuple[int, int] = (0, 0)
        self.obstacles: set = set()
        self.visited: set = set()

        for i in range(self.height):
            for j in range(self.width):
                if data[i][j] == UP:
                    self.guard = Guard(i, j)
                    self.start = (i, j)
                elif data[i][j] == OBSTACLE:
                    self.obstacles.add(Obstacle(i, j))

    def walk(self, add_visit: bool = True):
        """
        Walk the guard in the world.
        """
        x, y = self.guard.position_ahead()

        if any([o.x == x and o.y == y for o in self.obstacles]):
            self.guard.turn()
            return

        if add_visit:
            visit = (self.guard.x, self.guard.y)
            if visit not in self.visited:
                self.visited.add(visit)
        self.guard.move()

    def on_map(self, x, y) -> bool:
        """
        Check if the given coordinates are on the map.
        """
        return 0 <= x < self.height and 0 <= y < self.width

    def check_loop(self, obstacle: tuple[int, int]) -> bool:
        """
        Check if there is a loop in the world.
        :param obstacle: Obstacle to be added to create a time paradox.
        :return: True if there is a loop, False otherwise.
        """

        # Reset guard position and direction
        self.guard.direction = 0
        self.guard.x, self.guard.y = self.start

        # Locations and directions visited
        states = set()

        while self.on_map(self.guard.x, self.guard.y):
            # Add visited state
            states.add(((self.guard.x, self.guard.y), self.guard.direction))
            # Get position ahead

            # Turn if there is an obstacle or the position ahead is the obstacle
            while Obstacle(*self.guard.position_ahead()) in self.obstacles or self.guard.position_ahead() == obstacle:
                self.guard.turn()

            # If the position ahead and the direction is in the states, there is a loop
            if (self.guard.position_ahead(), self.guard.direction) in states:
                return True

            # Walk without changing the visited set
            self.walk(add_visit=False)

        return False


    def check_obstacles(self) -> int:
        """
        Check if there are obstacles to add to create a time paradox.
        :return: Number of obstacles to add.
        """
        obstacles_to_add = 0
        for obstacle in self.visited:
            if self.check_loop(obstacle):
                obstacles_to_add += 1
                print(".", end="")  # This takes a while
        return obstacles_to_add

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
        # world.print()
        world.walk()
        if not world.on_map(world.guard.x, world.guard.y):
            break

    world.print()
    world.print_stats()  # visited: 4647, obstacles: 807

    check_obstacles = world.check_obstacles()
    print(f"Obstacles to add: {check_obstacles}")  # 1723


if __name__ == "__main__":
    main()

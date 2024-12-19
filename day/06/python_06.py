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
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 0

    def move(self):
        x, y = DIRECTIONS[self.direction]
        self.x += x
        self.y += y

    def turn(self):
        self.direction = (self.direction + 1) % 4

    def position_ahead(self):
        x, y = DIRECTIONS[self.direction]
        return self.x + x, self.y + y

    def __str__(self):
        return DIRECTIONS_STR[self.direction]


class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return OBSTACLE


class World:
    def __init__(self, data):
        self.data = data
        self.start = (0, 0)
        self.guard = None
        self.obstacles = set()
        self.visited = set()
        self.height = len(data)
        self.width = len(data[0])

        for i in range(self.height):
            for j in range(self.width):
                if data[i][j] == UP:
                    self.start = (i, j)
                    self.guard = Guard(i, j)
                elif data[i][j] == OBSTACLE:
                    self.obstacles.add(Obstacle(i, j))

    def print(self):
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

    def walk(self):
        x, y = self.guard.position_ahead()

        if any([o.x == x and o.y == y for o in self.obstacles]):
            self.guard.turn()
            return

        visit = (self.guard.x, self.guard.y)
        if visit not in self.visited:
            self.visited.add(visit)
        self.guard.move()

    def on_map(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width

    def print_stats(self):
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

    world.print_stats()
    world.print()


if __name__ == "__main__":
    main()

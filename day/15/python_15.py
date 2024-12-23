from collections import namedtuple

# INPUT = "input_example_small.txt"
# INPUT = "input_example.txt"
INPUT = "input.txt"


WALL = "#"
EMPTY = "."
BOX = "O"
ROBOT = "@"

DIRECTIONS = {"^": (0, -1), ">": (1, 0), "v": (0, 1), "<": (-1, 0)}


def get_input() -> tuple[list[list[str]], str]:
    with open(INPUT) as f:
        data = f.read()
        map_data, instructions = data.split("\n\n")
        instructions = "".join(instructions.splitlines())
        return [list(line.strip()) for line in map_data.splitlines()], instructions


Location = namedtuple("Location", ["x", "y"])


class World:
    def __init__(self, map_data: list[list[str]]):
        self.height = len(map_data)
        self.width = len(map_data[0])
        self.map = map_data

        for y, row in enumerate(map_data):
            for x, cell in enumerate(row):
                if cell == ROBOT:
                    self.robot = Location(x, y)
                    self.map[y][x] = EMPTY

    def __str__(self):
        map_data = [line.copy() for line in self.map]
        map_data[self.robot.y][self.robot.x] = ROBOT
        return "\n".join(["".join(row) for row in map_data])

    def sum_box_gps(self):
        result = 0
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell == BOX:
                    result += (100 * y) + x
        return result

    def move_robot(self, direction: str):
        dx, dy = DIRECTIONS[direction]
        new_robot_pos = p = Location(self.robot.x + dx, self.robot.y + dy)

        if self.map[p.y][p.x] == WALL:
            # Do not move into walls
            return

        while self.map[p.y][p.x] == BOX:
            # Check all boxes can be moved together
            new_box_pos = Location(p.x + dx, p.y + dy)
            if self.map[new_box_pos.y][new_box_pos.x] == WALL:
                return
            p = new_box_pos

        while p != self.robot:
            # Swap boxes with empty space (in opposite direction)
            d = Location(p.x - dx, p.y - dy)
            self.map[p.y][p.x], self.map[d.y][d.x] = self.map[d.y][d.x], self.map[p.y][p.x]
            p = d

        self.robot = new_robot_pos


def main():
    map_data, instructions = get_input()
    world = World(map_data)
    for idx, instruction in enumerate(instructions, start=1):
        # print(f"Move {instruction}\t{idx}")
        world.move_robot(instruction)

    print(world)
    print()
    print(f"Sum of box GPS: {world.sum_box_gps()}")


if __name__ == "__main__":
    main()

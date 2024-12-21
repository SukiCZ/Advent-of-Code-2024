from collections import defaultdict
from itertools import combinations

# INPUT = "input_small.txt"
INPUT = "input.txt"


ANITONODE = "#"
EMPTY = "."


def read_input() -> list[str]:
    """
    Read the input file and return a list of strings
    """
    with open(INPUT) as f:
        return f.read().splitlines()


class Location:
    """
    A class to represent a location in the grid
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


class World:
    """
    A class to represent the world with antennas and antinodes

    Antennas are represented by their frequency (Single lower/upper/digit)
    """

    def __init__(self, data: list[str]):
        self.height: int = len(data)
        self.width: int = len(data[0])
        self.grid: list[list[str]] = [
            [EMPTY for _ in range(self.width)] for _ in range(self.height)
        ]
        self.antennas: dict[str, list[Location]] = defaultdict(list)
        self.antinodes: set[Location] = set()

        # Initialize the grid with antennas
        for i, row in enumerate(data):
            for j, cell in enumerate(row):
                # Add antennas to the grid if not empty
                if cell != EMPTY:
                    self.antennas[cell].append(Location(i, j))
                    self.grid[i][j] = cell

    def on_map(self, location: Location) -> bool:
        """
        Check if the location is on the map
        """
        return 0 <= location.x < self.height and 0 <= location.y < self.width

    def add_antinodes(self, location: Location, direction: Location):
        """
        Extend antinode positions in a direction (dx, dy)
        """
        ax, ay = location.x + direction.x, location.y + direction.y
        if self.on_map(Location(ax, ay)):
            # Antinodes can't overlap each other
            if self.grid[ax][ay] != ANITONODE:
                self.antinodes.add(Location(ax, ay))
                if self.grid[ax][ay] == EMPTY:
                    # Add to grid not to overlap with antennas
                    self.grid[ax][ay] = "#"

    def deploy_antinodes(self):
        """
        Deploy antinodes for all antennas

        For combination of each antenna pair, deploy antinodes in the direction of antenna pair
        """
        for antenna, locations in self.antennas.items():
            for loc_1, loc_2 in combinations(locations, 2):
                dx, dy = loc_2.x - loc_1.x, loc_2.y - loc_1.y
                self.add_antinodes(Location(loc_1.x, loc_1.y), Location(-dx, -dy))
                self.add_antinodes(Location(loc_2.x, loc_2.y), Location(dx, dy))

    def print(self):
        """
        Print the grid
        """
        for row in self.grid:
            print("".join(row))
        print("")


def main():
    data = read_input()
    world = World(data)
    # world.print()
    world.deploy_antinodes()
    # world.print()
    print(f"Lenght of antinodes: {len(world.antinodes)}")  # 332


if __name__ == "__main__":
    main()

# INPUT = "input_example_small.txt"  # 140, 80
# INPUT = "input_example.txt"  # 1930, 1206
INPUT = "input.txt"


def read_input():
    with open(INPUT) as f:
        return [line.strip() for line in f.readlines()]


class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        self.corner_directions = [
            (-1, -1),  # Up-Left
            (1, -1),  # Up-Right
            (-1, 1),  # Down-Left
            (1, 1),  # Down-Right
        ]
        self.visited = [[False for _ in range(self.width)] for _ in range(self.height)]

    def on_map(self, x: int, y: int) -> bool:
        """
        Check if the position is on the map
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def get_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """
        Get neighbors of the given position
        """
        return [
            (x + dx, y + dy)
            for dx, dy in self.directions
            if self.on_map(x + dx, y + dy)
            and self.grid[y + dy][x + dx] == self.grid[y][x]
            and not self.visited[y + dy][x + dx]
        ]

    def find_region(self, x: int, y: int) -> set[tuple[int, int]]:
        """
        Find the region of the given position
        """
        region = {(x, y)}
        self.visited[y][x] = True

        for dx, dy in self.get_neighbors(x, y):
            region.update(self.find_region(dx, dy))

        return set(region)

    def calculate_perimeter(self, region: set[tuple[int, int]]) -> int:
        """
        Calculate the perimeter of the region
        """
        perimeter = 0

        for x, y in region:
            for dx, dy in self.directions:
                if (x + dx, y + dy) not in region:
                    perimeter += 1
        return perimeter

    def calculate_corners(self, region: set[tuple[int, int]]) -> int:
        """
        Calculate the corners of the region
        """
        corners = 0

        for x, y in region:
            for dx, dy in self.corner_directions:

                # Inner corners
                if (x + dx, y) in region and (x, y + dy) in region and (x + dx, y + dy) not in region:
                    corners += 1

                # Outer corners
                if (x + dx, y) not in region and (x, y + dy) not in region:
                    corners += 1

        return corners

    def print(self):
        for row in self.grid:
            print(row)
        print()


def main():
    grid = Grid(read_input())
    # grid.print()
    perimeter_price_sum, corner_price_sum = 0, 0

    for y in range(grid.height):
        for x in range(grid.width):
            if not grid.visited[y][x]:
                region = grid.find_region(x, y)
                perimeter = grid.calculate_perimeter(region)
                corners = grid.calculate_corners(region)

                perimeter_price = perimeter * len(region)
                corner_price = corners * len(region)

                perimeter_price_sum += perimeter_price
                corner_price_sum += corner_price

                # print(f"Perimeter price: {perimeter_price}, Corner price: {corner_price} Region: {region}")

    print(f"Total perimeter price: {perimeter_price_sum}")
    print(f"Total corner price: {corner_price_sum}")


if __name__ == "__main__":
    main()

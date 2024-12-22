from __future__ import annotations

import re
from dataclasses import dataclass

# INPUT = "input_example.txt"
# WIDTH = 11
# HEIGHT = 7
INPUT = "input.txt"
WIDTH = 101
HEIGHT = 103

PATTERN = re.compile(r"p=(?P<px>-?\d+),(?P<py>-?\d+) v=(?P<vx>-?\d+),(?P<vy>-?\d+)")


def read_input() -> list[Robot]:
    result: list[Robot] = []
    with open(INPUT) as f:
        for line in f:
            match = PATTERN.match(line)
            if match:
                px, py, vx, vy = map(int, match.groups())
                result.append(Robot(position=Point(x=px, y=py), velocity=Point(x=vx, y=vy)))
    return result


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Robot:
    position: Point
    velocity: Point

    def move(self):
        self.position.x = (self.position.x + self.velocity.x) % WIDTH
        self.position.y = (self.position.y + self.velocity.y) % HEIGHT


@dataclass
class World:
    robots: list[Robot]

    def tick(self):
        for robot in self.robots:
            robot.move()

    def get_world(self) -> list[list[int]]:
        result = [[0] * WIDTH for _ in range(HEIGHT)]
        for robot in self.robots:
            result[robot.position.y][robot.position.x] += 1
        return result

    def sum_q(self, quarter: list[list[int]]) -> int:
        return sum(sum(line) for line in quarter)

    def count_quarters(self) -> tuple[int, int, int, int]:
        world = self.get_world()
        half_height = HEIGHT // 2
        half_width = WIDTH // 2
        top, bottom = world[:half_height], world[half_height + 1 :]
        q1 = [i[:half_width] for i in top]
        q2 = [i[half_width + 1 :] for i in top]
        q3 = [i[:half_width] for i in bottom]
        q4 = [i[half_width + 1 :] for i in bottom]
        return self.sum_q(q1), self.sum_q(q2), self.sum_q(q3), self.sum_q(q4)

    def print(self):
        print("\n".join("".join(str(line)) for line in self.get_world()))


def main():
    world = World(robots=read_input())
    for _ in range(100):
        world.tick()
    world.print()
    q1, q2, q3, q4 = world.count_quarters()
    safety_factory = q1 * q2 * q3 * q4
    print(f"Part 1: {safety_factory}")


if __name__ == "__main__":
    main()

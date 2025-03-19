"""utility imports"""
from utilities.runner import runner

@runner("Day 11", "Part 1")
def solve_part1(serial: int) -> str:
    """part 1 solving function"""
    grid = build_grid(serial)
    largest = None
    point = None
    for y in range(298):
        for x in range(298):
            p = 0
            for yo in range(3):
                for xo in range(3):
                    p += grid[y+yo][x+xo]
            if largest is None or p > largest:
                largest = p
                point = f"{x+1},{y+1}"
    return point

@runner("Day 11", "Part 2")
def solve_part2(serial: int) -> int:
    """part 2 solving function"""
    return 0

def build_grid(serial: int) -> list[list[int]]:
    """build power grid"""
    grid = []
    for y in range(300):
        row = []
        for x in range(300):
            row.append(power(serial, x+1, y+1))
        grid.append(row)
    return grid

def power(serial: int, x: int, y: int) -> int:
    """calculate power for the provided cell"""
    rack = x + 10
    p = rack * y
    p += serial
    p *= rack
    p = (p // 100) % 10
    p -= 5
    return p

# Part 1
assert power(8, 3, 5) == 4
assert power(57, 122, 79) == -5
assert power(39, 217, 196) == 0
assert power(71, 101, 153) == 4
assert solve_part1(18) == "33,45"
assert solve_part1(42) == "21,61"
assert solve_part1(7857) == "243,16"

# Part 2
assert solve_part2(18) == 0
assert solve_part2(7857) == 0

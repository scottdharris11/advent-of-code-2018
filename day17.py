"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 17", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    return 0

@runner("Day 17", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0

# Data
data = read_lines("input/day17/input.txt")
sample = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504""".splitlines()

# Part 1
assert solve_part1(sample) == 57
assert solve_part1(data) == 0

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0

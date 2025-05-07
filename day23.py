"""utility imports"""
import re
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 23", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    bots = parse_nanobots(lines)
    strongest = bots[0]
    for b in bots[1:]:
        if b[3] > strongest[3]:
            strongest = b
    in_range = 0
    for b in bots:
        if md(strongest, b) <= strongest[3]:
            in_range += 1
    return in_range

@runner("Day 23", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0

def md(a: tuple[int,int,int,int], b: tuple[int,int,int,int]) -> int:
    """compute manhattan distance between bots"""
    return abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2])

def parse_nanobots(lines: list[str]) -> list[tuple[int,int,int,int]]:
    """parse input text"""
    r = re.compile(r"pos=<([-\d]+),([-\d]+),([-\d]+)>, r=([\d]+)")
    nanobots = []
    for line in lines:
        s = r.search(line)
        bot = tuple((int(x) for x in s.groups()))
        nanobots.append(bot)
    return nanobots

# Data
data = read_lines("input/day23/input.txt")
sample = """pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1""".splitlines()

# Part 1
assert solve_part1(sample) == 7
assert solve_part1(data) == 780

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0

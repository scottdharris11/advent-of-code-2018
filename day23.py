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
    count = 0
    for b in bots:
        if in_range(strongest, b, strongest[3]):
            count += 1
    return count

@runner("Day 23", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    bots = parse_nanobots(lines)
    overlaps = {}
    print(f"bot count: {len(bots)}")
    for i1, b1 in enumerate(bots):
        for j, b2 in enumerate(bots[i1+1:]):
            i2 = i1+1+j
            print(f"looking for intersects between bot {i1} to {i2}")
            for i in intersects(b1, b2):
                o = overlaps.get(i, set())
                o.add(i1)
                o.add(i2)
                overlaps[i] = o
    #bots_by_range = []
    #for bidx, depends in overlaps.items():
    #    bots_by_range.append((bidx, len(depends)))
    #bots_by_range.sort(key=lambda x: x[1], reverse=True)
    return 0

def in_range(a: tuple[int,int,int], b: tuple[int,int,int], r: int) -> bool:
    """determine if the two positions"""
    return md(a, b) <= r

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

def intersects(b1: tuple, b2: tuple) -> set[tuple[int,int,int]]:
    """determine intersection points between two bots"""
    d = md(b1, b2)
    if b1[3] + b2[3] < d:
        return set()
    x_min, x_max = coordinate_range(b1[0], b1[3], b2[0], b2[3])
    y_min, y_max = coordinate_range(b1[1], b1[3], b2[1], b2[3])
    z_min, z_max = coordinate_range(b1[2], b1[3], b2[2], b2[3])
    b1_points = set()
    points(b1, (), b1[3], b1_points, (x_min, y_min, z_min), (x_max, y_max, z_max))
    b2_points = set()
    points(b2, (), b2[3], b2_points, (x_min, y_min, z_min), (x_max, y_max, z_max))
    return b1_points.intersection(b2_points)

def coordinate_range(c1: int, c1_range, c2: int, c2_range: int) -> tuple[int,int]:
    """determine the min/max range for the supplied coordinates based on the range"""
    min_range = max(c1 - c1_range, c2 - c2_range)
    max_range = min(c1 + c1_range, c2 + c2_range)
    return min_range, max_range

def points(base: tuple, p: tuple, remain: int, captured: set, mn: tuple, mx: tuple):
    """build reachable points for a bot"""
    bi = len(p)
    bp = base[bi]
    for r in range(remain*-1, remain+1):
        pp = bp+r
        if pp < mn[bi] or pp > mx[bi]:
            continue
        work = list(p)
        work.append(pp)
        if bi+1 == 3:
            captured.add(tuple(work))
        else:
            points(base, tuple(work), remain-abs(r), captured, mn, mx)

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
sample2 = """pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5""".splitlines()

# Part 1
assert solve_part1(sample) == 7
assert solve_part1(data) == 780

# Part 2
#assert solve_part2(sample2) == 36
assert solve_part2(data) == 0

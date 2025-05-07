"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 22", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    depth, target = parse_input(lines)
    regions = cave_regions(depth, target)
    risk = 0
    for y in range(target[1]+1):
        for x in range(target[0]+1):
            region = regions[(x,y)]
            risk += region.region_type
    return risk

@runner("Day 22", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0

ROCKY = 0
WET = 1
NARROW = 2

class Region:
    """defines structure for region attributes"""
    def __init__(self, loc: tuple[int,int], geo_idx: int, depth: int):
        self.loc = loc
        self.geo_idx = geo_idx
        self.erosin = erosin_level(geo_idx, depth)
        self.region_type = region_type(self.erosin)

    def __eq__(self, value):
        return self.loc == value.loc

    def __hash__(self):
        return hash(self.loc)

def geo_index(l: tuple[int,int], t: tuple[int,int], regions: dict[tuple[int,int],Region]) -> int:
    """compute the geo index for a location"""
    x, y = l
    if x == 0 and y == 0:
        return 0
    elif l == t:
        return 0
    elif y == 0:
        return x * 16807
    elif x == 0:
        return y * 48271
    return regions[(x-1,y)].erosin * regions[(x,y-1)].erosin

def erosin_level(geo_idx: int, depth: int) -> int:
    """compute the erosion level for a region"""
    return (geo_idx + depth) % 20183

def region_type(erosin: int) -> int:
    """compute the region type"""
    return erosin % 3

def cave_regions(depth: int, target: tuple[int,int]) -> dict[tuple[int,int],Region]:
    """build the cave regions based on the depth and target"""
    regions = {}
    for y in range(target[1]+1):
        for x in range(target[0]+1):
            loc = (x,y)
            geo = geo_index(loc, target, regions)
            regions[loc] = Region(loc, geo, depth)
    return regions

def parse_input(lines: list[str]) -> tuple[int,tuple[int,int]]:
    """parse the depth and target from input lines"""
    depth = int(lines[0][7:])
    t = lines[1][8:].split(",")
    target = (int(t[0]),int(t[1]))
    return depth, target

# Data
data = read_lines("input/day22/input.txt")
sample = """depth: 510
target: 10,10""".splitlines()

# Part 1
assert solve_part1(sample) == 114
assert solve_part1(data) == 9659

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0

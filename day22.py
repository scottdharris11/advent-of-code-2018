"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner
from utilities.search import Search, Searcher, SearchMove

@runner("Day 22", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    depth, target = parse_input(lines)
    cave = Cave(depth, target)
    risk = 0
    for y in range(target[1],-1,-1):
        for x in range(target[0],-1,-1):
            region = cave.region((x,y))
            risk += region.region_type
    return risk

@runner("Day 22", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    depth, target = parse_input(lines)
    cave = Cave(depth, target)
    cave.region(target)
    s = Search(PathSearcher(cave))
    solution = s.best(SearchMove(0,(0,0,TORCH)))
    return solution.cost

ROCKY = 0
WET = 1
NARROW = 2

NEITHER = 0
TORCH = 1
CLIMB_GEAR = 2

VALID_GEAR = {ROCKY: [TORCH,CLIMB_GEAR], WET: [NEITHER,CLIMB_GEAR], NARROW: [NEITHER,TORCH]}

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

class Cave:
    """defines structure for the cave"""
    def __init__(self, depth: int, target: tuple[int,int]):
        self.depth = depth
        self.target = target
        self.regions = {}

    def region(self, loc: tuple[int,int]) -> Region:
        """get the region for the location"""
        if loc not in self.regions:
            # map regions necessary to build the requested
            for y in range(loc[1]+1):
                for x in range(loc[0]+1):
                    loc = (x,y)
                    if loc in self.regions:
                        continue
                    geo = geo_index(loc, self.target, self.regions)
                    self.regions[loc] = Region(loc, geo, self.depth)
        return self.regions[loc]

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

def parse_input(lines: list[str]) -> tuple[int,tuple[int,int]]:
    """parse the depth and target from input lines"""
    depth = int(lines[0][7:])
    t = lines[1][8:].split(",")
    target = (int(t[0]),int(t[1]))
    return depth, target

class PathSearcher(Searcher):
    """path search implementation for the cave"""
    def __init__(self, cave: Cave) -> None:
        self.cave = cave
        self.goal = (self.cave.target[0], self.cave.target[1], TORCH)

    def is_goal(self, obj: tuple[int,int,int]) -> bool:
        """determine if the supplied state is the goal location"""
        return obj == self.goal

    def possible_moves(self, obj: tuple[int,int,int]) -> list[SearchMove]:
        """determine possible moves from curent location"""
        cloc = (obj[0], obj[1])
        cgear = obj[2]
        if cloc == self.cave.target:
            return [SearchMove(7,(obj[0],obj[1],TORCH))]
        moves = []
        for m in [(1,0),(-1,0),(0,1),(0,-1)]:
            loc = (obj[0] + m[0], obj[1] + m[1])
            if loc[0] < 0 or loc[1] < 0:
                continue
            cregion = self.cave.region((obj[0],obj[1]))
            crgear = VALID_GEAR[cregion.region_type]
            lregion = self.cave.region(loc)
            lrgear = VALID_GEAR[lregion.region_type]
            for g in lrgear:
                if g not in crgear:
                    continue
                if g == cgear:
                    moves.append(SearchMove(1,(loc[0],loc[1],g)))
                else:
                    moves.append(SearchMove(8,(loc[0],loc[1],g)))
        return moves

    def distance_from_goal(self, obj: tuple[int,int,int]) -> int:
        """calculate distance from the goal"""
        return abs(self.goal[0]-obj[0]) + abs(self.goal[1]-obj[1])

# Data
data = read_lines("input/day22/input.txt")
sample = """depth: 510
target: 10,10""".splitlines()

# Part 1
assert solve_part1(sample) == 114
assert solve_part1(data) == 9659

# Part 2
assert solve_part2(sample) == 45
assert solve_part2(data) == 1043

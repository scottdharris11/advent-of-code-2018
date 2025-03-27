"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 15", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    return 0

@runner("Day 15", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0

class Unit:
    """structure representing a battle unit"""
    def __init__(self, utype: chr, loc: tuple[int,int]):
        self.utype = utype
        self.loc = loc
        self.attack = 3
        self.hearts = 200

    def __repr__(self):
        return str((self.utype, self.loc, self.attack, self.hearts))

    def __lt__(self, other):
        x, y = self.loc
        ox, oy = other.loc
        if y == oy:
            return x < ox
        return y < oy

    def __eq__(self, other):
        return self.loc == other.loc

    def __attacked__(self, power: int) -> bool:
        """unit is attacked"""
        self.hearts -= power
        return self.hearts <= 0

class Map:
    """strucutre representing the map of the cave"""
    def __init__(self, lines: list[str]):
        self.walls = set()
        self.spaces = set()
        self.units = []
        for y, row in enumerate(lines):
            for x, col in enumerate(row):
                loc = (x,y)
                match col:
                    case '#':
                        self.walls.add(loc)
                    case '.':
                        self.spaces.add(loc)
                    case 'G' | 'E':
                        self.units.append(Unit(col, loc))

    def targets(self, unit: Unit) -> list[Unit]:
        """determine the available targets for the unit"""
        targets = []
        for u in self.units:
            if u.utype == unit.utype:
                continue
            targets.append(u)
        return targets

    def open_squares(self, targets: list[Unit]) -> set[tuple[int,int]]:
        """find open spaces around the supplied targets"""
        spaces = set()
        for t in targets:
            for move in [(-1,0),(0,-1),(0,1),(1,0)]:
                l = (t.loc[0]+move[0], t.loc[1]+move[1])
                if l in self.spaces:
                    spaces.add(l)
        return spaces

# Data
data = read_lines("input/day15/input.txt")
sample = """#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######""".splitlines()

# Part 1
assert solve_part1(sample) == 27730
assert solve_part1(data) == 0

# Part 2
assert solve_part2(data) == 0

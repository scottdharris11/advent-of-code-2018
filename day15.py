"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner
from utilities.search import Search, Searcher, SearchMove

@runner("Day 15", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    um = UnitMap(lines)
    rounds = 0
    while True:
        um.units.sort()
        died = False
        done = False
        for u in um.units:
            if u.hearts <= 0:
                continue
            ua = um.should_attack(u)
            if ua is None:
                t = um.targets(u)
                if len(t) == 0:
                    done = True
                    break
                spaces = um.open_squares(t)
                move = um.next_move(u, spaces)
                if move is not None:
                    um.move_unit(u, move)
                    ua = um.should_attack(u)
            if ua is not None:
                if ua.attacked(u.power):
                    um.remove_unit(ua)
                    died = True
        if died:
            nu = []
            for u in um.units:
                if u.hearts <= 0:
                    continue
                nu.append(u)
            um.units = nu
        if done:
            break
        rounds += 1
        #if rounds % 100 == 0:
        #print(f"after round {rounds}: {um.units}")
    health = 0
    for u in um.units:
        health += u.hearts
    return rounds * health

@runner("Day 15", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0

class Unit:
    """structure representing a battle unit"""
    def __init__(self, utype: chr, loc: tuple[int,int]):
        self.utype = utype
        self.loc = loc
        self.power = 3
        self.hearts = 200

    def __repr__(self):
        return str((self.utype, self.loc, self.power, self.hearts))

    def __lt__(self, other):
        x, y = self.loc
        ox, oy = other.loc
        if y == oy:
            return x < ox
        return y < oy

    def __eq__(self, other):
        return self.loc == other.loc

    def attacked(self, power: int) -> bool:
        """unit is attacked"""
        self.hearts -= power
        return self.hearts <= 0

class PathSearcher(Searcher):
    """path search implementation for the maze"""
    def __init__(self, spaces: set[tuple[int,int]], goal: tuple[int,int]) -> None:
        self.spaces = spaces
        self.goal = goal

    def is_goal(self, obj: tuple[int,int]) -> bool:
        """determine if the supplied state is the goal location"""
        return obj == self.goal

    def possible_moves(self, obj: tuple[int,int]) -> list[SearchMove]:
        """determine possible moves from curent location"""
        moves = []
        for m in [(1,0),(-1,0),(0,1),(0,-1)]:
            loc = (obj[0] + m[0], obj[1] + m[1])
            if loc not in self.spaces:
                continue
            moves.append(SearchMove(1,loc))
        return moves

    def distance_from_goal(self, obj: tuple[int,int]) -> int:
        """calculate distance from the goal"""
        return abs(self.goal[0]-obj[0]) + abs(self.goal[1]-obj[1])

class UnitMap:
    """strucutre representing the map of the cave"""
    def __init__(self, lines: list[str]):
        self.walls = set()
        self.spaces = set()
        self.units_by_loc = {}
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
                        self.units_by_loc[loc] = self.units[-1]

    def remove_unit(self, unit: Unit):
        """remove unit from the map"""
        current = unit.loc
        del self.units_by_loc[current]
        self.spaces.add(current)

    def move_unit(self, unit: Unit, loc: tuple[int,int]):
        """move the supplied unit to the supplied location"""
        current = unit.loc
        del self.units_by_loc[current]
        self.spaces.remove(loc)
        self.spaces.add(current)
        self.units_by_loc[loc] = unit
        unit.loc = loc

    def should_attack(self, unit: Unit) -> Unit:
        """determine if the supplied unit can attack and do so"""
        target = None
        for move in [(0,-1),(-1,0),(1,0),(0,1)]:
            l = (unit.loc[0]+move[0], unit.loc[1]+move[1])
            if l in self.units_by_loc:
                tu = self.units_by_loc[l]
                if tu.utype == unit.utype:
                    continue
                if target is None or tu.hearts < target.hearts:
                    target = tu
        return target

    def targets(self, unit: Unit) -> list[Unit]:
        """determine the available targets for the unit"""
        targets = []
        for u in self.units:
            if u.utype == unit.utype or u.hearts <= 0:
                continue
            targets.append(u)
        return targets

    def open_squares(self, targets: list[Unit]) -> set[tuple[int,int]]:
        """find open spaces around the supplied targets"""
        spaces = set()
        for t in targets:
            for move in [(0,-1),(-1,0),(1,0),(0,1)]:
                l = (t.loc[0]+move[0], t.loc[1]+move[1])
                if l in self.spaces:
                    spaces.add(l)
        return spaces

    def next_move(self, unit: Unit, goals: set[tuple[int,int]]) -> tuple[int,int]:
        """determine the next move for a unit"""
        nearest = 0
        best = None
        for goal in goals:
            ps = PathSearcher(self.spaces, goal)
            s = Search(ps)
            for move in [(0,-1),(-1,0),(1,0),(0,1)]:
                start = (unit.loc[0]+move[0], unit.loc[1]+move[1])
                if start not in self.spaces:
                    continue
                if start == goal:
                    if nearest == 0:
                        return goal
                md = abs(start[0]-goal[0]) + abs(start[1]-goal[1])
                if nearest > 0 and md > nearest:
                    continue
                s.cost_constraint = nearest
                solution = s.best(SearchMove(0, start))
                if solution is None:
                    continue
                if nearest == 0 or solution.cost < nearest:
                    nearest = solution.cost
                    best = start
        return best

# Data
data = read_lines("input/day15/input.txt")
sample = """#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######""".splitlines()
sample2 = """#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######""".splitlines()
sample3 = """#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######""".splitlines()
sample4 = """#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######""".splitlines()
sample5 = """#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######""".splitlines()
sample6 = """#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########""".splitlines()

# Part 1
assert solve_part1(sample) == 27730
assert solve_part1(sample2) == 36334
assert solve_part1(sample3) == 39514
assert solve_part1(sample4) == 27755
assert solve_part1(sample5) == 28944
assert solve_part1(sample6) == 18740
assert solve_part1(data) == 0 #<266496

# Part 2
assert solve_part2(data) == 0

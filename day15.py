"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner
from utilities.search import Search, Searcher, SearchMove

@runner("Day 15", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    return simulate(lines, 3, False)

@runner("Day 15", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    min_power = 4
    max_power = 100
    power = min_power
    scores = {}
    while True:
        if power in scores:
            result = scores[power]
        else:
            result = simulate(lines, power, True)
            scores[power] = result
        if result > 0:
            max_power = power
            if max_power == min_power or max_power - 1 == min_power:
                return result
        else:
            min_power = power
            if min_power + 1 == max_power:
                power = max_power
                continue
        power = min_power + ((max_power - min_power) // 2)


def simulate(lines: list[str], elf_power: int, elf_win: bool) -> int:
    """run game simulation"""
    um = UnitMap(lines, elf_power)
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
                spaces = um.open_squares(u, t)
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
                    if elf_win and u.utype == 'E':
                        return -1
                    continue
                nu.append(u)
            um.units = nu
        if done:
            break
        rounds += 1
    health = 0
    for u in um.units:
        health += u.hearts
    return rounds * health

class Unit:
    """structure representing a battle unit"""
    def __init__(self, utype: chr, loc: tuple[int,int], power: int):
        self.utype = utype
        self.loc = loc
        self.power = power
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
    def __init__(self, s: set[tuple[int,int]], g: tuple[int,int], c: tuple[int,int]) -> None:
        self.spaces = s
        self.goal = g
        self.current = c

    def is_goal(self, obj: tuple[int,int]) -> bool:
        """determine if the supplied state is the goal location"""
        return obj == self.goal

    def possible_moves(self, obj: tuple[int,int]) -> list[SearchMove]:
        """determine possible moves from curent location"""
        moves = []
        for m in [(1,0),(-1,0),(0,1),(0,-1)]:
            loc = (obj[0] + m[0], obj[1] + m[1])
            if loc not in self.spaces and loc != self.current:
                continue
            moves.append(SearchMove(1,loc))
        return moves

    def distance_from_goal(self, obj: tuple[int,int]) -> int:
        """calculate distance from the goal"""
        return abs(self.goal[0]-obj[0]) + abs(self.goal[1]-obj[1])

class UnitMap:
    """strucutre representing the map of the cave"""
    def __init__(self, lines: list[str], elf_power: int):
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
                    case 'G':
                        self.units.append(Unit(col, loc, 3))
                        self.units_by_loc[loc] = self.units[-1]
                    case 'E':
                        self.units.append(Unit(col, loc, elf_power))
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
        """determine if the supplied unit can attack and select target"""
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

    def open_squares(self, unit: Unit, targets: list[Unit]) -> list[tuple[tuple[int,int],int]]:
        """find open spaces around the supplied targets"""
        spaces = []
        for t in targets:
            for move in [(0,-1),(-1,0),(1,0),(0,1)]:
                l = (t.loc[0]+move[0], t.loc[1]+move[1])
                if l in self.spaces and l not in spaces:
                    rorder = (l[1]*1000) + l[0]
                    md = abs(unit.loc[0]-l[0]) + abs(unit.loc[1]-l[1])
                    sorder = (md * 100000) + rorder
                    spaces.append((l,sorder,rorder))
        spaces.sort(key=lambda x: x[1])
        return spaces

    def next_move(self, unit: Unit, spaces: list[tuple[tuple[int,int],int]]) -> tuple[int,int]:
        """determine the next move for a unit"""
        nearest = 0
        best = None
        rorder = 0
        for space in spaces:
            goal = space[0]
            ps = PathSearcher(self.spaces, goal, unit.loc)
            s = Search(ps)
            for move in [(0,-1),(-1,0),(1,0),(0,1)]:
                start = (unit.loc[0]+move[0], unit.loc[1]+move[1])
                if start not in self.spaces:
                    continue
                if start == goal:
                    if nearest == 0 or nearest > 1:
                        return goal
                md = abs(start[0]-goal[0]) + abs(start[1]-goal[1])
                if nearest > 0 and md > nearest:
                    continue
                s.cost_constraint = nearest
                solution = s.best(SearchMove(0, start))
                if solution is None:
                    continue
                if nearest == 0 or \
                   (solution.cost < nearest) or \
                   (solution.cost == nearest and space[2] < rorder):
                    nearest = solution.cost
                    best = start
                    rorder = space[2]
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
assert solve_part1(data) == 250648

# Part 2
assert solve_part2(sample) == 4988
assert solve_part2(sample3) == 31284
assert solve_part2(sample4) == 3478
assert solve_part2(sample5) == 6474
assert solve_part2(sample6) == 1140
assert solve_part2(data) == 42224

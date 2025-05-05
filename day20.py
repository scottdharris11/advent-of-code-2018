"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner
from utilities.search import Search, Searcher, SearchMove

@runner("Day 20", "Part 1")
def solve_part1(line: str) -> int:
    """part 1 solving function"""
    rooms = set()
    doors = set()
    rooms.add((0,0))
    chart_rooms(line[1:-1], (0,0), rooms, doors, set())
    locations = []
    for r in rooms:
        locations.append((md((0,0), r), r))
    locations.sort(key=lambda x: x[0])
    largest = 0
    while len(rooms) > 0:
        _, loc = locations.pop()
        if loc not in rooms:
            continue
        s = Search(PathSearcher(doors, loc))
        solution = s.best(SearchMove(0, (0,0)))
        if solution.cost > largest:
            largest = solution.cost
        for p in solution.path:
            if p in rooms:
                rooms.remove(p)
    return largest

@runner("Day 20", "Part 2")
def solve_part2(line: str) -> int:
    """part 2 solving function"""
    rooms = set()
    doors = set()
    rooms.add((0,0))
    chart_rooms(line[1:-1], (0,0), rooms, doors, set())
    locations = []
    for r in rooms:
        locations.append((md((0,0), r), r))
    locations.sort(key=lambda x: x[0])
    over1000 = 0
    while len(rooms) > 0:
        _, loc = locations.pop()
        if loc not in rooms:
            continue
        s = Search(PathSearcher(doors, loc))
        solution = s.best(SearchMove(0, (0,0)))
        for i, p in enumerate(solution.path):
            if p in rooms:
                if i >= 1000:
                    over1000 += 1
                rooms.remove(p)
    return over1000

MOVES = {'E': (1,0), 'W': (-1,0), 'N': (0,-1), 'S': (0,1)}
def chart_rooms(path: str, loc: tuple[int,int], rooms: set[tuple[int,int]], doors: set[tuple[int,int]], prev):
    """chart rooms and doors based on path"""
    explore = (loc, path)
    if len(path) == 0 or explore in prev:
        return
    prev.add(explore)
    for i, p in enumerate(path):
        if p == '(':
            pipes, se = split_breaks(path, i)
            wi = i
            for sp in pipes:
                chart_rooms(path[wi+1:sp]+path[se+1:], loc, rooms, doors, prev)
                wi = sp
            chart_rooms(path[wi+1:se]+path[se+1:], loc, rooms, doors, prev)
            break
        move = MOVES[p]
        loc = (loc[0]+move[0], loc[1]+move[1])
        doors.add(loc)
        loc = (loc[0]+move[0], loc[1]+move[1])
        rooms.add(loc)

def split_breaks(path: str, begin: int) -> tuple[list[int],int]:
    """find the ending index of the split that begins at supplied index"""
    stack = 0
    pipes = []
    for i in range(begin+1, len(path)):
        if path[i] == '(':
            stack += 1
        elif path[i] == ')':
            if stack == 0:
                return pipes, i
            stack -= 1
        elif path[i] == '|':
            if stack == 0:
                pipes.append(i)

def md(a: tuple[int,int], b: tuple[int,int]) -> int:
    """compute the manhattan distance between two points"""
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

class PathSearcher(Searcher):
    """path search implementation for the area"""
    def __init__(self, doors: set[tuple[int,int]], g: tuple[int,int]) -> None:
        self.doors = doors
        self.goal = g

    def is_goal(self, obj: tuple[int,int]) -> bool:
        """determine if the supplied state is the goal location"""
        return obj == self.goal

    def possible_moves(self, obj: tuple[int,int]) -> list[SearchMove]:
        """determine possible moves from curent location"""
        moves = []
        for m in [(1,0),(-1,0),(0,1),(0,-1)]:
            loc = (obj[0] + m[0], obj[1] + m[1])
            if loc not in self.doors:
                continue
            loc = (loc[0] + m[0], loc[1] + m[1])
            moves.append(SearchMove(1,loc))
        return moves

    def distance_from_goal(self, obj: tuple[int,int]) -> int:
        """calculate distance from the goal"""
        return md(self.goal, obj)

# Data
data = read_lines("input/day20/input.txt")[0]
sample = """^WNE$""".splitlines()[0]
sample2 = """^ENWWW(NEEE|SSE(EE|N))$""".splitlines()[0]
sample3 = """^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$""".splitlines()[0]
sample4 = """^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$""".splitlines()[0]
sample5 = """^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$""".splitlines()[0]

# Part 1
#assert solve_part1(sample) == 3
assert solve_part1(sample2) == 10
assert solve_part1(sample3) == 18
assert solve_part1(sample4) == 23
assert solve_part1(sample5) == 31
assert solve_part1(data) == 3725

# Part 2
assert solve_part2(data) == 8541

"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 20", "Part 1")
def solve_part1(line: str) -> int:
    """part 1 solving function"""
    rooms = set()
    doors = set()
    rooms.add((0,0))
    chart_rooms(line[1:-1], (0,0), rooms, doors, set())
    return 0

@runner("Day 20", "Part 2")
def solve_part2(line: str) -> int:
    """part 2 solving function"""
    return 0

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

# Data
data = read_lines("input/day20/input.txt")[0]
sample = """^WNE$""".splitlines()[0]
sample2 = """^ENWWW(NEEE|SSE(EE|N))$""".splitlines()[0]
sample3 = """^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$""".splitlines()[0]
sample4 = """^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$""".splitlines()[0]
sample5 = """^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$""".splitlines()[0]

# Part 1
#assert solve_part1(sample) == 3
#assert solve_part1(sample2) == 10
#assert solve_part1(sample3) == 18
#assert solve_part1(sample4) == 23
#assert solve_part1(sample5) == 31
assert solve_part1(data) == 0

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0

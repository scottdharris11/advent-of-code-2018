"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 18", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    area = []
    for line in lines:
        area.append(list(line))
    for _ in range(10):
        area = process_minute(area)
    woods = 0
    yards = 0
    for row in area:
        for acre in row:
            if acre == '|':
                woods += 1
            elif acre == '#':
                yards += 1
    return woods * yards

@runner("Day 18", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    area = []
    for line in lines:
        area.append(list(line))

    # locate spot where duplication begins
    sequence = []
    seen = {}
    minute = 0
    dup_at = 0
    while True:
        s = "".join("".join(a) for a in area)
        if s in seen:
            dup_at = seen[s]
            break
        sequence.append(s)
        seen[s] = minute
        area = process_minute(area)
        minute += 1

    # caluculate area offset that would hit at target minute
    # and use that area to calculate the resource value
    offset = (1000000000 - dup_at) % (minute-dup_at)
    woods = 0
    yards = 0
    for acre in sequence[dup_at + offset]:
        if acre == '|':
            woods += 1
        elif acre == '#':
            yards += 1
    return woods * yards

def process_minute(area: list[list[chr]]) -> list[list[chr]]:
    """process a minute"""
    size = len(area)
    work = [[' ' for _ in range(size)] for _ in range(size)]
    for y in range(size):
        for x in range(size):
            if area[y][x] == '|':
                work[y][x] = evaluate_tree(area, x, y)
            elif area[y][x] == '#':
                work[y][x] = evaluate_yard(area, x, y)
            else:
                work[y][x] = evaluate_open(area, x, y)
    return work

def evaluate_open(d: list[list[chr]], x: int, y: int) -> chr:
    """evaluate currently open acre"""
    trees = 0
    for offset in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
        nx = x + offset[0]
        ny = y + offset[1]
        if nx < 0 or nx >= len(d):
            continue
        if ny < 0 or ny >= len(d):
            continue
        if d[ny][nx] == '|':
            trees += 1
            if trees == 3:
                return '|'
    return d[y][x]

def evaluate_tree(d: list[list[chr]], x: int, y: int) -> chr:
    """evaluate acre of trees"""
    yards = 0
    for offset in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
        nx = x + offset[0]
        ny = y + offset[1]
        if nx < 0 or nx >= len(d):
            continue
        if ny < 0 or ny >= len(d):
            continue
        if d[ny][nx] == '#':
            yards += 1
            if yards == 3:
                return '#'
    return d[y][x]

def evaluate_yard(d: list[list[chr]], x: int, y: int) -> chr:
    """evaluate acre of lumberyard"""
    yard = False
    trees = False
    for offset in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
        nx = x + offset[0]
        ny = y + offset[1]
        if nx < 0 or nx >= len(d):
            continue
        if ny < 0 or ny >= len(d):
            continue
        if d[ny][nx] == '#':
            yard = True
        elif d[ny][nx] == '|':
            trees = True
        if yard and trees:
            return '#'
    return ' '

# Data
data = read_lines("input/day18/input.txt")
sample = """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.""".splitlines()

# Part 1
assert solve_part1(sample) == 1147
assert solve_part1(data) == 583426

# Part 2
assert solve_part2(data) == 169024

"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 6", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    coords = parse_coordinates(lines)
    min_x, min_y, max_x, max_y = None, None, None, None
    for x, y in coords:
        if min_x is None or x < min_x:
            min_x = x
        if max_x is None or x > max_x:
            max_x = x
        if min_y is None or y < min_y:
            min_y = y
        if max_y is None or y > max_y:
            max_y = y
    closest = {}
    pclosest = set()
    for x in range(min_x-1, max_x+2):
        for y in range(min_y-1, max_y+2):
            c = None
            cd = None
            for coord in coords:
                d = distance(coord, (x,y))
                if cd is None or d <= cd:
                    if d == cd:
                        c = "M"
                        continue
                    cd = d
                    c = coord
            if c == "M":
                continue
            points = closest.get(c, set())
            points.add((x,y))
            closest[c] = points
            perim = x == min_x-1 or x == max_x+1 or y == min_y-1 or y == max_y+1
            if perim:
                pclosest.add(c)
    flarge = None
    for k, c in closest.items():
        if k in pclosest:
            continue
        count = len(c)
        if flarge is None or count > flarge:
            flarge = count
    return flarge

@runner("Day 6", "Part 2")
def solve_part2(lines: list[str], constraint: int) -> int:
    """part 2 solving function"""
    coords = parse_coordinates(lines)
    min_x, min_y, max_x, max_y = None, None, None, None
    for x, y in coords:
        if min_x is None or x < min_x:
            min_x = x
        if max_x is None or x > max_x:
            max_x = x
        if min_y is None or y < min_y:
            min_y = y
        if max_y is None or y > max_y:
            max_y = y
    count = 0
    for x in range(min_x-1, max_x+2):
        for y in range(min_y-1, max_y+2):
            s = 0
            for coord in coords:
                s += distance(coord, (x,y))
                if s >= constraint:
                    break
            else:
                count += 1
    return count

def parse_coordinates(lines: list[str]) -> set[tuple[int,int]]:
    """parse coordinate set from input lines"""
    coords = set()
    for line in lines:
        c = line.split(", ")
        coords.add((int(c[0]), int(c[1])))
    return coords

def distance(a: tuple[int,int], b: tuple[int,int]) -> int:
    """calculate manhatten distance between coordinates"""
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

# Data
data = read_lines("input/day06/input.txt")
sample = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9""".splitlines()

# Part 1
assert solve_part1(sample) == 17
assert solve_part1(data) == 4754

# Part 2
assert solve_part2(sample, 32) == 16
assert solve_part2(data, 10000) == 42344

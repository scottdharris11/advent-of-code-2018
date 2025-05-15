"""utility imports"""
from utilities.data import read_lines, parse_integers
from utilities.runner import runner

@runner("Day 25", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    points = parse_points(lines)
    links = {}
    for i, a in enumerate(points):
        for b in points[i+1:]:
            if md(a,b) <= 3:
                l = links.get(a,set())
                l.add(b)
                links[a] = l
                l = links.get(b,set())
                l.add(a)
                links[b] = l
    count = 0
    assigned = set()
    for p in points:
        if p not in assigned:
            count += 1
            constellation(p, links, assigned)
    return count

def constellation(point, links, assigned):
    """assign points within constellations based on links"""
    if point in assigned:
        return
    assigned.add(point)
    if point not in links:
        return
    for link in links[point]:
        constellation(link, links, assigned)

def md(a: tuple[int,int,int,int], b: tuple[int,int,int,int]) -> int:
    """compute distance between two points"""
    return abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2]) + abs(a[3]-b[3])

def parse_points(lines: list[str]) -> list[tuple[int,int,int,int]]:
    """parse input lines"""
    points = []
    for line in lines:
        points.append(tuple(parse_integers(line,",")))
    return points

# Data
data = read_lines("input/day25/input.txt")
sample = """0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0""".splitlines()
sample2 = """-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0""".splitlines()
sample3 = """1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2""".splitlines()
sample4 = """1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2""".splitlines()

# Part 1
assert solve_part1(sample) == 2
assert solve_part1(sample2) == 4
assert solve_part1(sample3) == 3
assert solve_part1(sample4) == 8
assert solve_part1(data) == 383

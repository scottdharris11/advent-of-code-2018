"""utility imports"""
import re
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 10", "Part 1")
def solve_part1(lines: list[str]) -> str:
    """part 1 solving function"""
    msg, _ = find_message(lines)
    return msg

@runner("Day 10", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    _, seconds = find_message(lines)
    return seconds

class Light:
    """light position structure"""
    def __init__(self, x: int, y: int, vx: int, vy: int):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def next_position(self) -> tuple[int,int]:
        """move light to next position"""
        self.x += self.vx
        self.y += self.vy
        return (self.x, self.y)

    def __repr__(self):
        return str((self.x, self.y, self.vx, self.vy))

def parse_lights(lines: list[str]) -> list[Light]:
    """parse lights from input"""
    r = re.compile(r"position=<([ \-\d]+),([ \-\d]+)> velocity=<([ \-\d]+),([ \-\d]+)>")
    lights = []
    for line in lines:
        m = r.match(line)
        lights.append(Light(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))))
    return lights

def find_message(lines: list[str]) -> tuple[str,int]:
    """find encoded messsage in lights"""
    lights = parse_lights(lines)
    last = None
    previous = None
    seconds = 0
    while True:
        minx, maxx, miny, maxy = None, None, None, None
        positions = set()
        for light in lights:
            pos = light.next_position()
            positions.add(pos)
            x, y = pos
            if minx is None or x < minx:
                minx = x
            if maxx is None or x > maxx:
                maxx = x
            if miny is None or y < miny:
                miny = y
            if maxy is None or y > maxy:
                maxy = y
        yrange = maxy - miny + 1
        if last is not None and yrange > last:
            break
        last = yrange
        previous = positions
        seconds += 1
    output = ""
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            if (x,y) in previous:
                output += "#"
            else:
                output += "."
        output += "\n"
    return output, seconds

# Data
data = read_lines("input/day10/input.txt")
sample = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>""".splitlines()

# Part 1
assert solve_part1(sample) == """.............
..#...#..###.
..#...#...#..
..#...#...#..
..#####...#..
..#...#...#..
..#...#...#..
..#...#...#..
..#...#..###.
.............
.............
"""
assert solve_part1(data) == """......................................................................
......................................................................
......................................................................
......................................................................
......................................................................
.....#....#..#....#.....###..######....##....#....#....##....######...
.....#....#..#...#.......#...#........#..#...#...#....#..#...#........
.....#....#..#..#........#...#.......#....#..#..#....#....#..#........
.....#....#..#.#.........#...#.......#....#..#.#.....#....#..#........
.....######..##..........#...#####...#....#..##......#....#..#####....
.....#....#..##..........#...#.......######..##......######..#........
.....#....#..#.#.........#...#.......#....#..#.#.....#....#..#........
.....#....#..#..#....#...#...#.......#....#..#..#....#....#..#........
.....#....#..#...#...#...#...#.......#....#..#...#...#....#..#........
.....#....#..#....#...###....#.......#....#..#....#..#....#..#........
......................................................................
......................................................................
......................................................................
......................................................................
......................................................................
"""

# Part 2
assert solve_part2(sample) == 3
assert solve_part2(data) == 10888

"""utility imports"""
import re
from utilities.data import read_lines
from utilities.runner import runner

parse_y = re.compile(r"y=([0-9]+)(\.\.)*([0-9]+)*")
parse_x = re.compile(r"x=([0-9]+)(\.\.)*([0-9]+)*")

@runner("Day 17", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    clay, min_y, max_y = parse_clay(lines)
    water = flow(clay, max_y)
    #print_grid(clay, water)
    count = 0
    for l, _ in water.items():
        if l[1] >= min_y:
            count += 1
    return count

@runner("Day 17", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    clay, _, max_y = parse_clay(lines)
    water = flow(clay, max_y)
    #print_grid(clay, water)
    count = 0
    for _, w in water.items():
        if not w.flowing:
            count += 1
    return count

FLOW_DOWN = (0,1)
FLOW_LEFT = (-1,0)
FLOW_RIGHT = (1,0)

class Water:
    """represents a item of water"""
    def __init__(self, loc: tuple[int,int], source, flow_dir: tuple[int,int]):
        self.flowing = True
        self.loc = loc
        self.source = source
        self.flow_dir = flow_dir

    def __repr__(self):
        return str((self.loc, self.flowing))

def flow(clay: set[tuple[int,int]], max_y: int) -> dict[tuple[int,int],Water]:
    """initiate flow and count water"""
    queue = []
    current = Water((500,0), None, FLOW_DOWN)
    water = {}
    while True:
        below = (current.loc[0],current.loc[1]+1)
        if below[1] <= max_y:
            is_clay = below in clay
            is_water = below in water
            if not is_clay and not is_water:
                w = Water(below, current, FLOW_DOWN)
                water[w.loc] = w
                queue.append(w)
            elif is_water and water[below].flowing:
                pass
            else:
                if not current.flowing:
                    queue.append(current.source)
                elif current.flow_dir == FLOW_DOWN:
                    left = (current.loc[0]-1,current.loc[1])
                    left_clay = left in clay
                    left_water = left in water
                    left_water_stopped = left_water and not water[left].flowing
                    left_block = left_clay or left_water_stopped
                    right = (current.loc[0]+1,current.loc[1])
                    right_clay = right in clay
                    right_water = right in water
                    right_water_stopped = right_water and not water[right].flowing
                    right_block = right_clay or right_water_stopped
                    if left_block and right_block:
                        current.flowing = False
                        queue.append(current.source)
                    if not right_clay and not right_water:
                        w = Water(right, current, FLOW_RIGHT)
                        water[w.loc] = w
                        queue.append(w)
                    if not left_clay and not left_water:
                        w = Water(left, current, FLOW_LEFT)
                        water[w.loc] = w
                        queue.append(w)
                else:
                    next_loc = (current.loc[0]+current.flow_dir[0], current.loc[1])
                    if next_loc in clay or next_loc in water:
                        # check the reverse direction until hit either clay or no water.
                        # if clay encountered, then stop flow of all water points.
                        points = [current.loc]
                        reverse = current.flow_dir[0]*-1
                        prev_loc = current.loc
                        flow_stop = False
                        while True:
                            prev_loc = (prev_loc[0]+reverse, prev_loc[1])
                            if prev_loc in clay:
                                flow_stop = True
                                break
                            if prev_loc not in water:
                                break
                            points.append(prev_loc)
                        if flow_stop:
                            for p in points:
                                water[p].flowing = False
                        queue.append(current.source)
                    else:
                        w = Water(next_loc, current, current.flow_dir)
                        water[w.loc] = w
                        queue.append(w)
        if len(queue) == 0:
            break
        current = queue.pop()
    return water

def parse_clay(lines: list[str]) -> tuple[set[tuple[int,int]],int,int]:
    """parse clay locations from the supplied input"""
    clay = set()
    min_y = 0
    max_y = 0
    for line in lines:
        y_start, y_end = start_end_values(line, parse_y)
        if min_y == 0 or y_start < min_y:
            min_y = y_start
        if max_y == 0 or y_end > max_y:
            max_y = y_end
        x_start, x_end = start_end_values(line, parse_x)
        for x in range(x_start, x_end+1, 1):
            for y in range(y_start, y_end+1, 1):
                clay.add((x,y))
    return clay, min_y, max_y

def start_end_values(line: str, r: re.Pattern) -> tuple[int,int]:
    """parse start/end values from line using pattern"""
    match = r.findall(line)[0]
    start = int(match[0])
    end = start
    if match[2] != '':
        end = int(match[2])
    return start, end

def print_grid(clay: set[tuple[int,int]], water: dict[tuple[int,int],Water]):
    """print out the clay formations"""
    max_y = 0
    min_x = 0
    max_x = 0
    for c in clay:
        x, y = c
        if max_y == 0 or y > max_y:
            max_y = y
        if min_x == 0 or x < min_x:
            min_x = x
        if max_x == 0 or x > max_x:
            max_x = x
    for y in range(max_y+1):
        row = ""
        for x in range(min_x-1, max_x+2):
            loc = (x,y)
            if loc == (500,0):
                row += '+'
            elif loc in clay:
                row += '#'
            elif loc in water:
                if water[loc].flowing:
                    row += "|"
                else:
                    row += "~"
            else:
                row += '.'
        print(row)

# Data
data = read_lines("input/day17/input.txt")
sample = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504""".splitlines()

# Part 1
assert solve_part1(sample) == 57
assert solve_part1(data) == 29741

# Part 2
assert solve_part2(sample) == 29
assert solve_part2(data) == 24198

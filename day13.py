"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 13", "Part 1")
def solve_part1(lines: list[str]) -> str:
    """part 1 solving function"""
    cm = CartMap(lines)
    collision = "None"
    while True:
        c = cm.tick()
        if len(c) > 0:
            collision = f"{c[0][0]},{c[0][1]}"
            break
    return collision

@runner("Day 13", "Part 2")
def solve_part2(lines: list[str]) -> str:
    """part 2 solving function"""
    cm = CartMap(lines)
    last = "None"
    ticks = 0
    while True:
        cm.tick()
        ticks += 1
        if ticks % 1000000 == 0:
            print(f"tick {ticks}: ${cm.carts}")
        if len(cm.carts) == 1:
            last = f"{cm.carts[0].x},{cm.carts[0].y}"
        if len(cm.carts) <= 1:
            break
    return last

MOVES = {'>': (1,0), 'v': (0,1), '<': (-1,0), '^': (0,-1)}
DIRECTIONS = ['>', 'v', '<', '^']
TURNS = [-1, 0, 1]

class Cart:
    """represents a cart structure"""
    def __init__(self, x: int, y: int, direction: int):
        self.x = x
        self.y = y
        self.direction = direction
        self.turn = 0

    def __repr__(self):
        return str((self.x, self.y, self.direction, self.turn))

    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x
        return self.y < other.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def move(self, track: dict[tuple[int,int],chr]) -> tuple[int,int]:
        """move and turn the cart based on the track"""
        move_x, move_y = MOVES[DIRECTIONS[self.direction]]
        self.x += move_x
        self.y += move_y
        match track[(self.x, self.y)]:
            case '/':
                self.direction += 1 if DIRECTIONS[self.direction] in ['^','v'] else -1
            case '\\':
                self.direction += 1 if DIRECTIONS[self.direction] in ['>','<'] else -1
            case '+':
                self.direction += TURNS[self.turn]
                self.turn = (self.turn + 1) % len(TURNS)
        if self.direction < 0:
            self.direction = len(DIRECTIONS)-1
        elif self.direction == len(DIRECTIONS):
            self.direction = 0
        return self.x, self.y

class CartMap:
    """represents a track structure"""
    def __init__(self, lines: list[str]):
        self.track = {}
        self.carts = []
        for y, row in enumerate(lines):
            for x, col in enumerate(row):
                if col in ['|', '-', '\\', '/', '+']:
                    self.track[(x,y)] = col
                elif col in DIRECTIONS:
                    self.track[(x,y)] = "-"
                    self.carts.append(Cart(x, y, DIRECTIONS.index(col)))

    def tick(self) -> list[tuple[int,int]]:
        """move carts a tick and detect collisions"""
        collisions = []
        crashed = []
        self.carts.sort()
        for i, c in enumerate(self.carts):
            l = c.move(self.track)
            for ci, cc in enumerate(self.carts):
                if i == ci:
                    continue
                if c == cc:
                    collisions.append(l)
                    crashed.append(i)
                    crashed.append(ci)
        if len(crashed) > 0:
            ncarts = []
            for i, c in enumerate(self.carts):
                if i in crashed:
                    continue
                ncarts.append(c)
            self.carts = ncarts
        return collisions

# Data
data = read_lines("input/day13/input.txt")
sample = r"""/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   """.splitlines()
sample2 = r"""/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/""".splitlines()

# Part 1
assert solve_part1(sample) == "7,3"
assert solve_part1(data) == "129,50"

# Part 2
assert solve_part2(sample) == "None"
assert solve_part2(sample2) == "6,4"
assert solve_part2(data) == "69,73"

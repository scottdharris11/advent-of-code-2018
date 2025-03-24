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
        if c is not None:
            collision = f"{c[0]},{c[1]}"
            break
    return collision

@runner("Day 13", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0

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
        """move the cart based on the track"""
        move = MOVES[DIRECTIONS[self.direction]]
        self.x += move[0]
        self.y += move[1]
        match track[(self.x, self.y)]:
            case '|' | '-':
                return self.x, self.y
            case '/':
                self.direction += 1 if DIRECTIONS[self.direction] in ['^','v'] else -1
            case '\\':
                self.direction += 1 if DIRECTIONS[self.direction] in ['>','<'] else -1
            case '+':
                self.direction += TURNS[self.turn]
                self.turn += 1
                if self.turn == len(TURNS):
                    self.turn = 0
        if self.direction < 0:
            self.direction = len(DIRECTIONS)-1
        if self.direction >= len(DIRECTIONS):
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

    def tick(self) -> tuple[int,int]:
        """move carts a tick and detect collisions"""
        collisions = []
        locations = set()
        self.carts.sort()
        for c in self.carts:
            l = c.move(self.track)
            if l in locations:
                collisions.append(l)
            locations.add(l)
        if len(collisions) > 0:
            return collisions[0]
        return None

# Data
data = read_lines("input/day13/input.txt")
sample = r"""/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   """.splitlines()

# Part 1
assert solve_part1(sample) == "7,3"
assert solve_part1(data) == "129,50"

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0

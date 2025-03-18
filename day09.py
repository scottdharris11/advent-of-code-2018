"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 9", "Part 1")
def solve_part1(players: int, last: int) -> int:
    """part 1 solving function"""
    current = Marble(0)
    current.next = current
    current.prev = current
    scores = [0] * players
    player = 0
    for i in range(1, last+1):
        if i % 23 == 0:
            scores[player] += i
            remove = current
            for _ in range(7):
                remove = remove.prev
            scores[player] += remove.identifier
            left = remove.prev
            right = remove.next
            left.next = right
            right.prev = left
            current = right
        else:
            m = Marble(i)
            left = current.next
            right = left.next
            left.next = m
            m.prev = left
            right.prev = m
            m.next = right
            current = m
        player = (player + 1) % players
    return max(scores)

@runner("Day 9", "Part 2")
def solve_part2(players: int, marbles: int) -> int:
    """part 2 solving function"""
    return 0

class Marble:
    """marble structure"""
    def __init__(self, identifier: int):
        self.identifier = identifier
        self.next = None
        self.prev = None

# Data
data = read_lines("input/day09/input.txt")
sample = """""".splitlines()

# Part 1
assert solve_part1(9, 25) == 32
assert solve_part1(10, 1618) == 8317
assert solve_part1(13, 7999) == 146373
assert solve_part1(17, 1104) == 2764
assert solve_part1(21, 6111) == 54718
assert solve_part1(30, 5807) == 37305
assert solve_part1(426, 72058) == 424112

# Part 2
assert solve_part2(9, 25) == 0
assert solve_part2(426, 72058) == 0

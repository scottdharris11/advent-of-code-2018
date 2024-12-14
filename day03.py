"""utility imports"""
import re
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 3", "Part 1")
def solve_part1(claims: list[str]):
    """part 1 solving function"""
    claimed = {}
    for c in claims:
        claim = Claim(c)
        for x in range(claim.x, claim.x + claim.width, 1):
            for y in range(claim.y, claim.y + claim.height, 1):
                loc = (x, y)
                claimed[loc] = claimed.get(loc, 0) + 1
    overlap = 0
    for v in claimed.values():
        if v > 1:
            overlap += 1
    return overlap

@runner("Day 3", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    claimed = {}
    claims = []
    for c in lines:
        claim = Claim(c)
        claims.append(claim)
        for x in range(claim.x, claim.x + claim.width, 1):
            for y in range(claim.y, claim.y + claim.height, 1):
                loc = (x, y)
                claimed[loc] = claimed.get(loc, 0) + 1
    for claim in claims:
        overlap = False
        for x in range(claim.x, claim.x + claim.width, 1):
            for y in range(claim.y, claim.y + claim.height, 1):
                loc = (x, y)
                if claimed[loc] > 1:
                    overlap = True
                    break
            if overlap:
                break
        if not overlap:
            return claim.id
    return 0

claim_extract = re.compile(r'#([0-9]*) @ ([0-9]*),([0-9]*): ([0-9]*)x([0-9]*)')

class Claim:
    """claim definition"""
    def __init__(self, s: str) -> None:
        s = claim_extract.search(s)
        self.id = int(s.group(1))
        self.x = int(s.group(2))
        self.y = int(s.group(3))
        self.width = int(s.group(4))
        self.height = int(s.group(5))

    def __repr__(self):
        return str((self.id, self.x, self.y, self.width, self.height))

# Data
data = read_lines("input/day03/input.txt")
sample = """#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2""".splitlines()

# Part 1
assert solve_part1(sample) == 4
assert solve_part1(data) == 100595

# Part 2
assert solve_part2(sample) == 3
assert solve_part2(data) == 415

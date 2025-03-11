"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 5", "Part 1")
def solve_part1(line: str):
    """part 1 solving function"""
    return len(reduce(line))

@runner("Day 5", "Part 2")
def solve_part2(line: str):
    """part 2 solving function"""
    min_polymer = None
    for i in range(26):
        c = chr(ord('a') + i)
        s = len(reduce(clean(line, c)))
        if min_polymer is None or s < min_polymer:
            min_polymer = s
    return min_polymer

def reduce(polymer: str) -> str:
    """reduce the colliding polymers"""
    start = 0
    while True:
        for i in range(start, len(polymer)-1):
            collide = False
            c = polymer[i]
            if c.islower():
                collide = c.upper() == polymer[i+1]
            else:
                collide = c.lower() == polymer[i+1]
            if collide:
                start = i-1
                polymer = polymer[:i] + polymer[i+2:]
                break
        else:
            break
    return polymer

def clean(polymer: str, unit: chr) -> str:
    """clean the supplied polymer of supplied units"""
    uunit = str(unit).upper()[0]
    output = ""
    for c in polymer:
        if c == unit or c == uunit:
            continue
        output += c
    return output

# Data
data = read_lines("input/day05/input.txt")[0]
sample = """dabAcCaCBAcCcaDA""".splitlines()[0]

# Part 1
assert solve_part1(sample) == 10
assert solve_part1(data) == 11754

# Part 2
assert solve_part2(sample) == 4
assert solve_part2(data) == 4098

"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 2", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    appear2 = 0
    appear3 = 0
    for line in lines:
        cnt_by_letters = {}
        for c in line:
            cnt_by_letters[c] = cnt_by_letters.get(c, 0) + 1
        if 2 in cnt_by_letters.values():
            appear2 += 1
        if 3 in cnt_by_letters.values():
            appear3 += 1
    return appear2 * appear3

@runner("Day 2", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    return 0

# Data
data = read_lines("input/day02/input.txt")
sample = """abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab""".splitlines()

# Part 1
assert solve_part1(sample) == 12
assert solve_part1(data) == 5704

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0

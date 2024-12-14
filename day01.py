"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 1", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    return sum(map(int, lines))

@runner("Day 1", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    vals = list(map(int, lines))
    seen = set()
    s = 0
    seen.add(s)
    i = 0
    while True:
        s += vals[i]
        if s in seen:
            return s
        seen.add(s)
        i = (i + 1) % len(vals)

# Data
data = read_lines("input/day01/input.txt")
sample = """+1
-2
+3
+1""".splitlines()
sample2 = """+1
+1
+1""".splitlines()
sample3 = """+1
+1
-2""".splitlines()
sample4 = """-1
-2
-3""".splitlines()
sample5 = """+1
-1""".splitlines()
sample6 = """+3
+3
+4
-2
-4""".splitlines()
sample7 = """-6
+3
+8
+5
-6""".splitlines()
sample8 = """+7
+7
-2
-7
-4""".splitlines()

# Part 1
assert solve_part1(sample) == 3
assert solve_part1(sample2) == 3
assert solve_part1(sample3) == 0
assert solve_part1(sample4) == -6
assert solve_part1(data) == 556

# Part 2
assert solve_part2(sample) == 2
assert solve_part2(sample5) == 0
assert solve_part2(sample6) == 10
assert solve_part2(sample7) == 5
assert solve_part2(sample8) == 14
assert solve_part2(data) == 448

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
    l = len(lines)
    for i in range(l):
        for j in range(i+1,l,1):
            diff = set()
            for x, c in enumerate(lines[i]):
                if c != lines[j][x]:
                    diff.add(c)
                    if len(diff) > 1:
                        break
            if len(diff) == 1:
                return lines[i].replace(diff.pop(),"")
    return ""

# Data
data = read_lines("input/day02/input.txt")
sample = """abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab""".splitlines()
sample2 = """abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz""".splitlines()

# Part 1
assert solve_part1(sample) == 12
assert solve_part1(data) == 5704

# Part 2
assert solve_part2(sample2) == "fgij"
assert solve_part2(data) == "umdryabviapkozistwcnihjqx"

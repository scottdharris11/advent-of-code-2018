"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 12", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    state, rules = parse_input(lines)
    zero_idx = 0
    for _ in range(20):
        # using current state, look for rule matches to spread plants
        work = ".." + state + ".."
        l = len(work)
        ns = ""
        for i, _ in enumerate(work):
            comp = ""
            if i < 2:
                comp = "." * (2-i)
                comp += work[0:i+3]
            elif i >= l - 2:
                comp = work[i-2:]
                comp += "." * (3-(l-i))
            else:
                comp = work[i-2:i+3]
            pot = comp in rules
            ns += "#" if pot else "."

        # prune state and adjust zero index if necessary
        if ns[0] == "#":
            zero_idx += 2
        elif ns [1] == "#":
            zero_idx += 1
            ns = ns[1:]
        else:
            ns = ns[2:]
        for p in range(len(ns)-1,-1,-1):
            if ns[p] == "#":
                ns = ns[:p+1]
                break
        state = ns

    # sum pop total, offsetting for adjusted zero index
    pots = 0
    for i, p in enumerate(state):
        if p == '#':
            pots += i - zero_idx
    return pots

@runner("Day 8", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0

def parse_input(lines: list[str]) -> tuple[list[str],set[str]]:
    """parse input"""
    initial = lines[0][15:]
    rules = set()
    for line in lines[2:]:
        pattern = line[:5]
        if line[9] == '#':
            rules.add(pattern)
    return initial, rules

# Data
data = read_lines("input/day12/input.txt")
sample = """initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #""".splitlines()

# Part 1
assert solve_part1(sample) == 325
assert solve_part1(data) == 2444

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0

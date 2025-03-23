"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 12", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    state, rules = parse_input(lines)
    state, zero_idx = state_after(state, rules, 20)
    return sum_pots(state, zero_idx)

@runner("Day 8", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    state, rules = parse_input(lines)
    state, zero_idx = state_after(state, rules, 50000000000)
    return sum_pots(state, zero_idx)

def parse_input(lines: list[str]) -> tuple[list[str],set[str]]:
    """parse input"""
    initial = lines[0][15:]
    rules = set()
    for line in lines[2:]:
        pattern = line[:5]
        if line[9] == '#':
            rules.add(pattern)
    return initial, rules

def state_after(state: str, rules: set[str], generations: int) -> tuple[str,int]:
    """compute the plant state of a supplied number of generations"""
    zero_idx = 0
    steps = []
    seen = set()
    for g in range(generations):
        next_state, zero_adjust = generation(state, rules)
        # detect repeating pattern of plants, and the applied zero offset
        # and then simulate those generations versus actually computing them.
        # as it turned out, the repeating pattern was only one step, so the
        # logic is simplified more than it would need to be if the repeating
        # pattern was multiple steps.
        if next_state in seen:
            for i, s in enumerate(steps):
                if next_state == s[0]:
                    repeat_adjust = 0
                    for step in steps[i:]:
                        repeat_adjust += step[1]
                    simulate = generations - g
                    zero_idx += repeat_adjust * simulate
                    break
            break
        steps.append((next_state, zero_adjust))
        seen.add(next_state)
        state = next_state
        zero_idx += zero_adjust
    return state, zero_idx

def generation(state: str, rules: set[str]) -> tuple[str,int]:
    """determine state and zero offset adjust for next generation"""
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
    zero_adjust = 2
    for i, p in enumerate(ns):
        if p == "#":
            zero_adjust -= i
            ns = ns[i:]
            break
    for p in range(len(ns)-1,-1,-1):
        if ns[p] == "#":
            ns = ns[:p+1]
            break
    return ns, zero_adjust

def sum_pots(state: str, zero_idx: int) -> int:
    """sum set of pot indexes, offsetting for adjusted zero index"""
    pots = 0
    for i, p in enumerate(state):
        if p == '#':
            pots += i - zero_idx
    return pots

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
assert solve_part2(data) == 750000000697

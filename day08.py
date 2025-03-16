"""utility imports"""
from utilities.data import read_lines, parse_integers
from utilities.runner import runner

@runner("Day 8", "Part 1")
def solve_part1(line: str) -> int:
    """part 1 solving function"""
    values = parse_integers(line, " ")
    ms, _ = metadata(values)
    return ms

@runner("Day 8", "Part 2")
def solve_part2(line: str) -> int:
    """part 2 solving function"""
    return 0

def metadata(values: list[int]) -> tuple[int,int]:
    """calculate the sum of metadata within the node values"""
    ms = 0
    n_count = values[0]
    m_count = values[1]
    idx = 2
    for _ in range(n_count):
        m, i = metadata(values[idx:])
        ms += m
        idx += i
    ms += sum(values[idx:idx+m_count])
    return ms, idx + m_count

# Data
data = read_lines("input/day08/input.txt")[0]
sample = """2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2""".splitlines()[0]

# Part 1
assert solve_part1(sample) == 138
assert solve_part1(data) == 44893

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0

"""utility imports"""
import re
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 4", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    r = re.compile(r"\[\d+-\d+-\d+ \d+:(\d+)")
    amount_by_guard = {}
    mins_by_guard = {}
    guard = None
    start = None
    lines.sort()
    for line in lines:
        if line.endswith("begins shift"):
            guard = int(line[line.index("#")+1:-12])
            continue
        minute = int(r.match(line).group(1))
        if line.endswith("falls asleep"):
            start = minute
        else:
            amount_by_guard[guard] = amount_by_guard.get(guard,0) + (minute-start)
            sleep_mins = mins_by_guard.get(guard,{})
            for m in range(start,minute):
                sleep_mins[m] = sleep_mins.get(m,0) + 1
            mins_by_guard[guard] = sleep_mins
    max_guard = None
    max_amount = None
    for g, m in amount_by_guard.items():
        if max_amount is None or m > max_amount:
            max_amount = m
            max_guard = g
    sleep_mins = mins_by_guard[max_guard]
    max_minute = None
    max_amount = None
    for m, a in sleep_mins.items():
        if max_amount is None or a > max_amount:
            max_amount = a
            max_minute = m
    return max_guard * max_minute

@runner("Day 4", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0

# Data
data = read_lines("input/day04/input.txt")
sample = """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:25] wakes up
[1518-11-02 00:40] falls asleep
[1518-11-01 00:30] falls asleep
[1518-11-05 00:45] falls asleep
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-01 00:05] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:46] wakes up
[1518-11-02 00:40] falls asleep
[1518-11-05 00:55] wakes up""".splitlines()

# Part 1
assert solve_part1(sample) == 240
assert solve_part1(data) == 73646

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0

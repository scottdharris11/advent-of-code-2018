"""utility imports"""
import re
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 7", "Part 1")
def solve_part1(lines: list[str]) -> str:
    """part 1 solving function"""
    queue, steps, depends = parse_steps(lines)
    order = ""
    while len(queue) > 0:
        queue.sort(reverse=True)
        step = queue.pop()
        order += step
        for s in depends.get(step, []):
            prereqs = steps.get(s, [])
            prereqs.remove(step)
            if len(prereqs) == 0:
                queue.append(s)
            steps[s] = prereqs
    return order

@runner("Day 7", "Part 2")
def solve_part2(lines: list[str], workers: int, duration: int):
    """part 2 solving function"""
    queue, steps, depends = parse_steps(lines)
    seconds = 0
    inprogress = {}
    while len(queue) > 0 or len(inprogress) > 0:
        remove = []
        for i, d in inprogress.items():
            if d == seconds:
                for s in depends.get(i, []):
                    prereqs = steps.get(s, [])
                    prereqs.remove(i)
                    if len(prereqs) == 0:
                        queue.append(s)
                    steps[s] = prereqs
                remove.append(i)
        for r in remove:
            del inprogress[r]
        while len(queue) > 0 and len(inprogress) < workers:
            queue.sort(reverse=True)
            step = queue.pop()
            inprogress[step] = seconds + duration + (ord(step) - ord('A') + 1)
        seconds += 1
    return seconds - 1

def parse_steps(lines: list[str]) -> tuple[list[str],dict[str,list[str]],dict[str,list[str]]]:
    """parse the step dependencies from the input"""
    queue = []
    steps = {}
    depends = {}
    extract = re.compile(r"Step ([A-Z]) must be finished before step ([A-Z]) can begin.")
    for line in lines:
        match = extract.match(line)
        step = match.group(2)
        depend = match.group(1)
        prereqs = steps.get(step, [])
        prereqs.append(depend)
        steps[step] = prereqs
        after = depends.get(depend, [])
        after.append(step)
        depends[depend] = after
        if depend not in steps and depend not in queue:
            queue.append(depend)
        if step in queue:
            queue.remove(step)
    return queue, steps, depends

# Data
data = read_lines("input/day07/input.txt")
sample = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""".splitlines()

# Part 1
assert solve_part1(sample) == "CABDFE"
assert solve_part1(data) == "LFMNJRTQVZCHIABKPXYEUGWDSO"

# Part 2
assert solve_part2(sample, 2, 0) == 15
assert solve_part2(data, 5, 60) == 1180

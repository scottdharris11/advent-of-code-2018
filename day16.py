"""utility imports"""
from utilities.data import read_lines, parse_integers
from utilities.runner import runner

@runner("Day 16", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    samples, _ = parse_input(lines)
    threeplus = 0
    for s in samples:
        before = parse_integers(s[0][9:len(s[0])-1], ",")
        expected = parse_integers(s[2][9:len(s[2])-1], ",")
        operation = s[1]
        matched = 0
        for f in [addr,addi,mulr,muli,banr,bani,borr,bori,setr,seti,gtir,gtri,gtrr,eqir,eqri,eqrr]:
            if match(f, before, expected, operation) >= 0:
                matched += 1
        if matched >= 3:
            threeplus += 1
    return threeplus

@runner("Day 16", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    samples, ops = parse_input(lines)
    poperations = {}
    for s in samples:
        before = parse_integers(s[0][9:len(s[0])-1], ",")
        expected = parse_integers(s[2][9:len(s[2])-1], ",")
        operation = s[1]
        for f in [addr,addi,mulr,muli,banr,bani,borr,bori,setr,seti,gtir,gtri,gtrr,eqir,eqri,eqrr]:
            opcd = match(f, before, expected, operation)
            if opcd >= 0:
                opcds = poperations.get(f, set())
                opcds.add(opcd)
                poperations[f] = opcds
    operations = determine_opcodes(poperations)
    registers = {0:0, 1:0, 2:0, 3:0}
    for op in ops:
        opcode, a, b, c, *_ = parse_integers(op, " ")
        func = operations[opcode]
        func(registers, a, b, c)
    return registers[0]

def parse_input(lines: list[str]) -> tuple[list[list[str]], list[str]]:
    """parse input into sections"""
    samples = []
    index = 0
    while True:
        if index >= len(lines) or not lines[index].startswith("Before:"):
            break
        samples.append(list(lines[index:index+3]))
        index += 4
    index += 2
    return samples, list(lines[index:])

def determine_opcodes(poperations) -> dict:
    """determine operation codes by eliminating items appliciable to one code iteratively"""
    operations = {}
    while True:
        todelete = []
        for f, opcodes in poperations.items():
            if len(opcodes) == 1:
                code = list(opcodes)[0]
                for f2, popcodes in poperations.items():
                    if f == f2:
                        continue
                    if code in popcodes:
                        popcodes.remove(code)
                todelete.append(f)
                operations[code] = f
        for d in todelete:
            del poperations[d]
        if len(poperations) == 0:
            break
    return operations

def match(f, before: list[int], expected: list[int], operation: str) -> int:
    """determine if the supplied function results in the expected register values"""
    registers = dict(enumerate(before))
    opcode, a, b, c, *_ = parse_integers(operation, " ")
    f(registers, a, b, c)
    for i, v in enumerate(expected):
        if registers[i] != v:
            return -1
    return opcode

def addr(r: dict[int,int], a: int, b: int, c: int):
    """add register"""
    r[c] = r[a] + r[b]

def addi(r: dict[int,int], a: int, b: int, c: int):
    """add immediate"""
    r[c] = r[a] + b

def mulr(r: dict[int,int], a: int, b: int, c: int):
    """multiply register"""
    r[c] = r[a] * r[b]

def muli(r: dict[int,int], a: int, b: int, c: int):
    """multiply immediate"""
    r[c] = r[a] * b

def banr(r: dict[int,int], a: int, b: int, c: int):
    """bitwise AND register"""
    r[c] = r[a] & r[b]

def bani(r: dict[int,int], a: int, b: int, c: int):
    """bitwise AND immediate"""
    r[c] = r[a] & b

def borr(r: dict[int,int], a: int, b: int, c: int):
    """bitwise OR register"""
    r[c] = r[a] | r[b]

def bori(r: dict[int,int], a: int, b: int, c: int):
    """bitwise OR immediate"""
    r[c] = r[a] | b

def setr(r: dict[int,int], a: int, _: int, c: int):
    """set register"""
    r[c] = r[a]

def seti(r: dict[int,int], a: int, _: int, c: int):
    """set immediate"""
    r[c] = a

def gtir(r: dict[int,int], a: int, b: int, c: int):
    """greater-than immediate/register"""
    r[c] = 1 if a > r[b] else 0

def gtri(r: dict[int,int], a: int, b: int, c: int):
    """greater-than register/immediate"""
    r[c] = 1 if r[a] > b else 0

def gtrr(r: dict[int,int], a: int, b: int, c: int):
    """greater-than register/register"""
    r[c] = 1 if r[a] > r[b] else 0

def eqir(r: dict[int,int], a: int, b: int, c: int):
    """equal immediate/register"""
    r[c] = 1 if a == r[b] else 0

def eqri(r: dict[int,int], a: int, b: int, c: int):
    """equal register/immediate"""
    r[c] = 1 if r[a] == b else 0

def eqrr(r: dict[int,int], a: int, b: int, c: int):
    """equal register/register"""
    r[c] = 1 if r[a] == r[b] else 0

# Data
data = read_lines("input/day16/input.txt")
sample = """Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]""".splitlines()

# Part 1
assert solve_part1(sample) == 1
assert solve_part1(data) == 509

# Part 2
assert solve_part2(data) == 496

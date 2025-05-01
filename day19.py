"""utility imports"""
from utilities.data import read_lines, parse_integers
from utilities.runner import runner

@runner("Day 19", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    ins_register = int(lines[0][4:])
    instructions = lines[1:]
    registers = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0}
    while True:
        ins_idx = registers[ins_register]
        if ins_idx < 0 or ins_idx >= len(instructions):
            break
        instruction = instructions[ins_idx]
        cmd = COMMANDS[instruction[0:4]]
        a, b, c, *_ = parse_integers(instruction[5:], " ")
        cmd(registers, a, b, c)
        registers[ins_register] = registers[ins_register] + 1
    return registers[0]

@runner("Day 19", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0

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

COMMANDS = {
    "addr": addr, "addi":addi, "mulr": mulr, "muli": muli, 
    "banr": banr, "bani": bani, "borr": borr, "bori": bori, 
    "setr": setr, "seti": seti, "gtir": gtir, "gtri": gtri, 
    "gtrr": gtrr, "eqir": eqir, "eqri": eqri, "eqrr": eqrr
}

# Data
data = read_lines("input/day19/input.txt")
sample = """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5""".splitlines()

# Part 1
assert solve_part1(sample) == 7
assert solve_part1(data) == 1806

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0

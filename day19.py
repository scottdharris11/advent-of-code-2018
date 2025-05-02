"""utility imports"""
from utilities.data import read_lines, parse_integers
from utilities.runner import runner

@runner("Day 19", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    registers = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0}
    execute(registers, int(lines[0][4:]), lines[1:])
    return registers[0]

@runner("Day 19", "Part 2")
def solve_part2(base: int) -> int:
    """part 2 solving function"""
    # program first computes a base number:
    #   when 0 (part 1), it is 1028
    #   when 1, it is 10551428
    # then it finds all of the even divisors of it and adds them
    # to the output register 0, but without using a modulus operator.
    # simulating that behavior here to arrive at the number.
    output = 1 + base
    for i in range(2, (base//2)+1):
        if base % i == 0:
            output += i
    return output

def execute(registers: dict[int,int], ins_register: int, instructions: list[str]):
    """execute the program until completion"""
    while True:
        ins_idx = registers[ins_register]
        if ins_idx < 0 or ins_idx >= len(instructions):
            break
        instruction = instructions[ins_idx]
        cmd = COMMANDS[instruction[0:4]]
        a, b, c, *_ = parse_integers(instruction[5:], " ")
        cmd(registers, a, b, c)
        registers[ins_register] = registers[ins_register] + 1

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
assert solve_part2(1028) == 1806
assert solve_part2(10551428) == 18741072

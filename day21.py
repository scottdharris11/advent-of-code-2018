"""utility imports"""
from utilities.runner import runner

@runner("Day 21", "Part 1")
def solve_part1() -> int:
    """part 1 solving function"""
    # not taking input as part of this as we are just simulating
    # a program based on the input (not using it directly).
    # commands from the input can be seen implemented in day 19 script.
    #
    # in the first part, we are trying to determine what the value
    # of register 0 needs to be at the start of the program in order
    # for it to exit as quickly as possible. Register 0 is only used
    # in one command of the program at it is a comparison against
    # register 1 at that point and if equal the program will effectively
    # halt, so we are looking for the value of register one at the
    # moment that command would have run.
    #
    # Program has three 3 loops within it:
    #   - large outer loop that begins at command index 6 (value at register 2 drives)
    #     - stops when value of register 1 equals register 0
    #     - in part 1, we only want this loop to run once (not a loop below)
    #   - first inner loop that begins at command index 8 and runs through index 27
    #     - stops when value of register 2 is less than 256 (command index 13)
    #   - second inner loop that begins at command index 18 and runs through 25
    #     - stops when value of register 4 is greater than register 2 (command index 20)
    r1 = 0 # commands 0-5 (setup)
    r2 = r1 | 65536 #command 6
    r1 = 10605201 # command 7
    while True:
        r5 = r2 & 255 # command 8
        r1 = (((r1 + r5) & 16777215) * 65899) & 16777215 # commands 9-12
        if r2 < 256: # commands 13,14,16,28
            break
        r5 = 0 # command 17
        # inner loop (commands 18-25)
        while True:
            r4 = (r5 + 1) * 256 # commands 18-19
            if r4 > r2: # command 20
                break # commands 21, 23
            r5 += 1 # command 24
        r2 = r5 # command 26
    return r1

@runner("Day 21", "Part 2")
def solve_part2() -> int:
    """part 2 solving function"""
    return 0

# Part 1
assert solve_part1() == 11592302

# Part 2
assert solve_part2() == 0

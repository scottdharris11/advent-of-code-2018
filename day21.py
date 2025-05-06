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
    # for it to exit as quickly as possible. Register 0 is consulted
    # at the end of the main loop and compared against the value that
    # is in Register 1 and when equal, program will end.  So, for part
    # 1, we will simulate the logic for part 1 once and then return.
    return main_loop(0)

@runner("Day 21", "Part 2")
def solve_part2() -> int:
    """part 2 solving function"""
    # not taking input as part of this as we are just simulating
    # a program based on the input (not using it directly).
    # commands from the input can be seen implemented in day 19 script.
    #
    # in part 2, knowing that the program as it exists will be an
    # infinite loop, we are looking for a value that will stop the main
    # loop after as many instructions as possible.  Interpreting this
    # as finding all outputs of register 1 until a duplicate is found
    # that would send the program into the infinite loop.  So we will
    # find when the program would have started to loop (duplicate output
    # of register 1), and then use the previous register 1 value to
    # effectively stop the program as far along the path as we can.
    seen = set()
    prev = None
    r1 = 0
    while True:
        r1 = main_loop(r1)
        if r1 in seen:
            break
        seen.add(r1)
        prev = r1
    return prev

def main_loop(r1: int) -> int:
    """main loop logic"""
    # Program has three 3 loops within it:
    #   - large outer loop that begins at command index 6
    #     - stops when value of register 1 equals register 0
    #   - first inner loop that begins at command index 8 and runs through index 27
    #     - stops when value of register 2 is less than 256 (command index 13)
    #   - second inner loop that begins at command index 18 and runs through 25
    #     - stops when value of register 4 is greater than register 2 (command index 20)
    r2 = r1 | 65536 #command 6
    r1 = 10605201 # command 7
    while True:
        r5 = r2 & 255 # command 8
        r1 = (((r1 + r5) & 16777215) * 65899) & 16777215 # commands 9-12
        if r2 < 256: # commands 13,14,16,28
            break
        r2 = r2 // 256 # inner loop (commands 17-25)
    return r1

# Part 1
assert solve_part1() == 11592302

# Part 2
assert solve_part2() == 313035

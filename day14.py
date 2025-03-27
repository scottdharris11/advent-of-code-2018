"""utility imports"""
from utilities.runner import runner

@runner("Day 14", "Part 1")
def solve_part1(count: int) -> str:
    """part 1 solving function"""
    recipes = [3, 7]
    elf1 = 0
    elf2 = 1
    while len(recipes) < count + 10:
        r = recipes[elf1] + recipes[elf2]
        if r < 10:
            recipes.append(r)
        else:
            recipes.append(1)
            recipes.append(r-10)
        elf1 = next_index(elf1, recipes[elf1], len(recipes))
        elf2 = next_index(elf2, recipes[elf2], len(recipes))
    return "".join(map(str,recipes[count:count+10]))

@runner("Day 14", "Part 2")
def solve_part2(count: int) -> str:
    """part 2 solving function"""
    return ""

def next_index(i: int, r: int, l: int) -> int:
    """determine the next elf index"""
    i += r + 1
    while i >= l:
        i -= l
    return i

# Part 1
assert solve_part1(9) == "5158916779"
assert solve_part1(5) == "0124515891"
assert solve_part1(18) == "9251071085"
assert solve_part1(2018) == "5941429882"
assert solve_part1(236021) == "6297310862"

# Part 2
assert solve_part2(236021) == ""

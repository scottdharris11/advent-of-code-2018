"""utility imports"""
import re
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 24", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    immune, infection = run_simulation(lines, 0)
    return immune + infection

@runner("Day 24", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    boost_min = 0
    boost_max = 1000
    win_found = False
    while True:
        boost = boost_min + (boost_max - boost_min) // 2
        immune, _ = run_simulation(lines, boost)
        if immune == 0:
            boost_min = boost + 1
            if not win_found:
                boost_max += 500
        else:
            win_found = True
            boost_max = boost
            if boost_max == boost_min:
                return immune

def run_simulation(lines: list[str], boost: int) -> tuple[int,int]:
    """run simulation with supplied boost"""
    immune, infection = parse_groups(lines)
    for i in immune:
        i.attack += boost
    while len(immune) > 0 and len(infection) > 0:
        # targeting stage
        immune.sort(key=lambda g: g.effective_power(), reverse=True)
        infection.sort(key=lambda g: g.effective_power(), reverse=True)
        targeted = set()
        for i in immune:
            t = i.target_select(infection, targeted)
            if t > -1:
                targeted.add(t)
        targeted = set()
        for i in infection:
            t = i.target_select(immune, targeted)
            if t > -1:
                targeted.add(t)

        # attacking stage
        groups = []
        groups.extend(immune)
        groups.extend(infection)
        groups.sort(key=lambda g: g.initiative, reverse=True)
        groupUpdated = False
        for g in groups:
            if g.units == 0:
                continue
            if g.target is None:
                continue
            before = g.target.units
            g.target.attacked(g.would_damage(g.target))
            if g.target.units < before:
                groupUpdated = True

        # check for stalemate (infection wins)
        if not groupUpdated:
            infection_remain = 0
            for i in infection:
                infection_remain += i.units
            return 0, infection_remain

        # count remaining groups
        for i in range(len(immune)-1,-1,-1):
            if immune[i].units == 0:
                immune.pop(i)
        for i in range(len(infection)-1,-1,-1):
            if infection[i].units == 0:
                infection.pop(i)

    # count remaining units
    immune_remain = 0
    for i in immune:
        immune_remain += i.units
    infection_remain = 0
    for i in infection:
        infection_remain += i.units
    return immune_remain, infection_remain

class Group:
    """structure representing unit group"""
    def __init__(self, u: int, p: int, a: int, at: int, it: int, w: list[str], im: list[str]):
        self.units = u
        self.power = p
        self.attack = a
        self.attack_type = at
        self.initiative = it
        self.weakness = w
        self.immunities = im
        self.target = None

    def effective_power(self) -> int:
        """effective power of the group"""
        return self.units * self.attack

    def target_select(self, groups: list, prev_selected: set[int]) -> int:
        """select the target based on rules"""
        self.target = None
        best = -1
        damage = -1
        for i, group in enumerate(groups):
            if i in prev_selected or group.units == 0:
                continue
            d = self.would_damage(group)
            if d > 0 and (damage == -1 or d > damage):
                best = i
                damage = d
            elif d == damage:
                if group.effective_power() > groups[best].effective_power():
                    best = i
                elif group.effective_power() == groups[best].effective_power():
                    if group.initiative > groups[best].initiative:
                        best = i
        if best >= 0:
            self.target = groups[best]
        return best

    def would_damage(self, group) -> int:
        """determine the damage that would be done to group"""
        m = 1
        if self.attack_type in group.weakness:
            m = 2
        elif self.attack_type in group.immunities:
            m = 0
        return m * self.effective_power()

    def attacked(self, damage: int) -> bool:
        """group is attacked"""
        ud = damage // self.power
        if ud >= self.units:
            self.units = 0
            return True
        self.units -= ud
        return False

def parse_groups(lines: list[str]) -> tuple[list[Group],list[Group]]:
    """parse groups from input"""
    p = re.compile(r"([\d]+) units each with ([\d]+) hit points (\([\s\S]+\) )?with an attack that does ([\d]+) ([a-z]+) damage at initiative ([\d]+)")
    immune = []
    infection = []
    active = immune
    for line in lines[1:]:
        if line == "":
            continue
        if line == "Infection:":
            active = infection
            continue
        m = p.match(line)
        groups = m.groups()
        units = int(groups[0])
        power = int(groups[1])
        wi = groups[2]
        attack = int(groups[3])
        attack_type = groups[4]
        initiative = int(groups[5])
        weakness = []
        immunities = []
        if wi is not None:
            for chunk in wi[1:-2].split("; "):
                if chunk.startswith("weak to "):
                    weakness = chunk[8:].split(", ")
                else:
                    immunities = chunk[10:].split(", ")
        active.append(Group(units, power, attack, attack_type, initiative, weakness, immunities))
    return immune, infection

# Data
data = read_lines("input/day24/input.txt")
sample = """Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4""".splitlines()

# Part 1
assert solve_part1(sample) == 5216
assert solve_part1(data) == 23385

# Part 2
assert solve_part2(sample) == 51
assert solve_part2(data) == 2344

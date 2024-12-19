#!/usr/bin/env python3

import sys


def parse_towels(lines):
    lines = lines[:]
    towels = lines.pop(0).strip().split(', ')
    lines.pop(0)

    designs = []
    for line in lines:
        designs.append(line.strip()) 

    return towels, designs


def is_possible_design(design, towels):
    max_len = max([len(t) for t in towels])
    min_len = min([len(t) for t in towels])

    stack = [design]
    while stack:
        des = stack.pop()
        if des in towels:
            return True

        for n in range(min_len, max_len+1):
            head = des[:n]
            if head in towels:
                stack.append(des[n:])

    return False


def minimize_towel_set(towels):
    towels = set(towels)
    min_towels = set()

    for towel in towels:
        new_towels = towels.copy()
        new_towels.remove(towel)

        if not is_possible_design(towel, new_towels):
            min_towels.add(towel)

    return min_towels


def possible_designs(designs, towels):
    towels = minimize_towel_set(towels)

    possible = []
    for design in designs:
        if is_possible_design(design, towels):
            possible.append(design)

    return possible

def part1(lines):
    towels, designs = parse_towels(lines)
    possible = possible_designs(designs, towels)
    return len(possible)


def part2(lines):
    pass


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


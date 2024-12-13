#!/usr/bin/env python3

import sys
from operator import itemgetter


def parse_xy(line):
    first, second = line.strip().split(", ")
    x = int(first[2:], 10)
    y = int(second[2:], 10)
    return (x, y)


def parse_machines(lines):
    lines = lines[:]
    machines = []
    while lines:
        first = lines.pop(0)
        if not first.strip():
            continue

        second = lines.pop(0)
        third = lines.pop(0)

        a = parse_xy(first[9:])
        b = parse_xy(second[9:])
        prize = parse_xy(third[6:])

        machines.append((a, b, prize))

    return machines


def solve_machine(machine):
    (ax, ay), (bx, by), (px, py) = machine
    max_a = min(px / ax, py / ay)
    max_b = min(px / bx, py / by)
    
    a_count = int(max_a)

    solves = []
    while a_count >= 0:
        x1, y1 = ax * a_count, ay * a_count

        b_count = 0
        while b_count <= max_b:
            x2, y2 = bx * b_count, by * b_count
            x, y = x1 + x2, y1 + y2

            if x == px and y == py:
                solves.append((a_count, b_count, (3 * a_count) + b_count))
            if x > px or y > py:
                break

            b_count += 1

        a_count -= 1

    if not len(solves):
        return None

    solves.sort(key=itemgetter(2))
    return solves[0]


def part1(lines):
    machines = parse_machines(lines)
    solves = [solve_machine(machine) for machine in machines]
    return sum(solve[2] for solve in solves if solve is not None)


def part2(lines):
    pass


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


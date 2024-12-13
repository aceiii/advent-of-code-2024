#!/usr/bin/env python3

import sys
from operator import itemgetter
from math import floor


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


def solve_linear_equation1(machine):
    (ax, ay), (bx, by), (px, py) = machine

    # equation taken from reddit...
    ec = by*px
    bf = bx*py
    ea = by*ax
    bd = bx*ay
    x = (ec - bf) / (ea - bd)

    if x != floor(x):
        return None

    if bx == 0 or by == 0:
        return None

    y = (px - (x * ax)) / bx
    y2 = (py - (x * ay)) / by

    if y != y2:
        return None

    return x, y


def solve_linear_equation(machine):
    (ax, ay), (bx, by), (px, py) = machine

    da = ax-ay
    db = bx-by
    dp = px - py
    nx = dp / da
    cy = -(db / da)

    n = ax * nx
    ny = (ax * cy) + bx
    p = px - n
    y = round(p / ny, 3)
    x = round((px - (y * bx)) / ax, 3)

    """
    ans = solve_linear_equation1(machine)
    if ans is not None:
        xx, yy = ans
        if xx != x and yy != y:
            print('mismatch', xx, yy, x, y)
    """

    return x, y


def solve_machine_linear(machine):
    ans = solve_linear_equation(machine)
    if ans is None:
        return None

    x, y = ans

    if x != int(x) or y != int(y):
        return None

    c = int((x * 3) + y)
    return (x, y, c)


def part1(lines):
    machines = parse_machines(lines)
    solves = [solve_machine(machine) for machine in machines]
    return sum(solve[2] for solve in solves if solve is not None)


def part2(lines):
    t = 10000000000000
    machines = parse_machines(lines)
    solves = [solve_machine_linear((a, b, (px + t, py + t))) for a, b, (px, py) in machines]
    return sum(solve[2] for solve in solves if solve is not None)


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


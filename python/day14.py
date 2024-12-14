#!/usr/bin/env python3

import sys


def parse_robots(lines):
    bots = []
    for line in lines:
        first, second = line.strip().split(" ")
        pos = tuple(int(x, 10) for x in first[2:].split(","))
        vel = tuple(int(x, 10) for x in second[2:].split(","))
        bots.append((pos, vel))
    return bots


def sim(bots, dims):
    w, h = dims
    new_bots = []
    for pos, vel in bots:
        x, y = pos
        vx, vy = vel
        new_pos = ((x + vx) % w, (y + vy) % h)
        new_bots.append((new_pos, vel))
    return new_bots


def bot_quadrants(bots, dims):
    quadrants = {
        (0, 0): 0,
        (0, 1): 0,
        (1, 1): 0,
        (1, 0): 0
    }


    w, h = dims
    mx = w // 2
    my = h // 2

    for (x, y), _ in bots:
        if x == mx or y == my:
            continue

        qx, qy = 0, 0
        if x > mx:
            qx = 1
        if y > my:
            qy = 1

        quadrants[(qx, qy)] += 1


    return list(quadrants.values())


def part1(lines):
    dims = (101, 103)
    bots = parse_robots(lines)

    for _ in range(100):
        bots = sim(bots, dims)

    a, b, c, d = bot_quadrants(bots, dims)
    return a * b * c * d


def part2(lines):
    pass


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


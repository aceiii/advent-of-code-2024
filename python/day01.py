#!/usr/bin/env python3

import sys
import re
from collections import defaultdict


def part1(lines):
    first = []
    second = []
    for line in lines:
        a, b = re.split(r"\W+", line.strip())
        first.append(int(a, 10))
        second.append(int(b, 10))

    first.sort()
    second.sort()
    diffs = (abs(b - a) for a, b in zip(first, second))
    return sum(diffs)


def part2(lines):
    first = []
    second = defaultdict(lambda: 0)
    for line in lines:
        a, b = re.split(r"\W+", line.strip())
        first.append(int(a, 10))
        second[int(b, 10)] += 1

    return sum(a *second[a] for a in first)


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


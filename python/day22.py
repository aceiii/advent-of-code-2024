#!/usr/bin/env python3

import sys


def next_secret(n):
    a = (n ^ (n * 64)) % 16777216
    b = (a ^ (a // 32)) % 16777216
    c = (b ^ (b * 2048)) % 16777216
    return c


def gen_secret(i, n):
    s = i
    while n:
        s = next_secret(s)
        n -= 1
    return s


def part1(lines):
    t = 2000
    inits = [int(line, 10) for line in lines]
    secrets = [gen_secret(i, t) for i in inits]
    return sum(secrets)



def part2(lines):
    pass


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


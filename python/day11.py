#!/usr/bin/env python3

import sys


def flatten(lst):
    return [x for xs in lst for x in xs]


def count_digits(n):
    even = False
    digits = 1
    while n >= 10:
        even = not even
        n = n // 10
        digits += 1
    return digits, even


def blink(n):
    if n == 0:
        return [1]
    
    digits, even = count_digits(n)
    if even:
        e = digits // 2
        m = 10**e
        return [n // m, n % m]

    return [n * 2024]


def part1(lines):
    stones = [int(a, 10) for a in lines[0].strip().split(' ')]
    for _ in range(25):
        new_stones = flatten(blink(a) for a in stones)
        stones = new_stones
    return len(stones)

def part2(lines):
    pass


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


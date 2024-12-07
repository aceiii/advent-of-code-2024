#!/usr/bin/env python3

import sys
from math import log


def add(a, b):
    return a + b


def mul(a, b):
    return a * b


def concat(a, b):
    exp = int(log(b, 10)) + 1
    return (a * 10**exp) + b


def apply_operators(nums, ops, target):
    nums = nums[:]
    results = [nums.pop(0)]

    while nums:
        b = nums.pop(0)

        new_results = []
        while results:
            a = results.pop(0)
            for op in ops:
                c = op(a, b)
                if c > target:
                    continue
                new_results.append(c)
        results = new_results

    for res in results:
        yield res


def part1(lines):
    answer = 0
    for line in lines[:]:
        first, rest = line.strip().split(":")
        result = int(first, 10)
        nums = [int(n, 10) for n in rest.strip().split(" ")]
        for val in apply_operators(nums, [add, mul], result):
            if val == result:
                answer += result
                break

    return answer


def part2(lines):
    answer = 0
    for line in lines[:]:
        first, rest = line.strip().split(":")
        result = int(first, 10)
        nums = [int(n, 10) for n in rest.strip().split(" ")]
        for val in apply_operators(nums, [add, mul, concat], result):
            if val == result:
                answer += result
                break

    return answer


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


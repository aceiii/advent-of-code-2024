#!/usr/bin/env python3

import sys
from operator import itemgetter
from collections import defaultdict


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


def gen_prices(i, n):
    prices = [(i, i % 10, None)]
    s = i
    while n:
        ns = next_secret(s)
        np = ns % 10
        cp = np - prices[-1][1]
        n -= 1
        s = ns
        prices.append((ns, np, cp))
    return prices


def part2(lines):
    t = 2000
    inits = [int(line, 10) for line in lines]
    prices = [gen_prices(i, t) for i in inits]


    global_sequence = defaultdict(lambda: 0)

    for price in prices:
        sv = set()
        for i in range(len(price) - 4):
            cs = tuple(c for _,_,c in price[i:i+4])
            p = price[i+3][1]

            if cs not in sv:
                sv.add(cs)
                global_sequence[cs] += p

    sequences = sorted(global_sequence.items(), key=itemgetter(1), reverse=True)
    sequence, count = sequences[0]
    return count


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


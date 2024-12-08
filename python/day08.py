#!/usr/bin/env python3

import sys
import string
from collections import defaultdict


def parse_map(lines):
    freq_map = defaultdict(lambda: set())
    height = len(lines)
    width = len(lines[0])

    print(width, height)

    for y, line in enumerate(lines):
        for x, c in enumerate(line.strip()):
            pos = (x, y)
            if c != '.':
                freq_map[c].add(pos)

    return freq_map, (width, height)


def within_bounds(dims, pos):
    w, h = dims
    x, y = pos
    return x >= 0 and y >= 0 and x < w and y < h


def print_map(dims, freq_map, antinodes):
    w, h = dims 
    objs = {}

    for c in freq_map:
        freqs = freq_map[c]
        for pos in freqs:
            objs[pos] = c

    for pos in antinodes:
        objs[pos] = '#'

    for y in range(h):
        line = []
        for x in range(w):
            pos = (x, y)
            if pos in objs:
                line.append(objs[pos])
            else:
                line.append('.')
        print("".join(line))


def part1(lines):
    freq_map, dims = parse_map(lines)
    antinodes = set()

    for c in freq_map:
        freq_set = freq_map[c]
        freqs = list(freq_set)

        for idx, f1 in enumerate(freqs[:-1]):
            for f2 in freqs[idx + 1:]:
                x1, y1 = f1
                x2, y2 = f2
                dx, dy = x2 - x1, y2 - y1

                a1 = x1 - dx, y1 - dy
                a2 = x2 + dx, y2 + dy

                if within_bounds(dims, a1) and a1 not in freqs:
                    antinodes.add(a1)

                if within_bounds(dims, a2) and a2 not in freqs:
                    antinodes.add(a2)


    return len(antinodes)


def part2(lines):
    freq_map, dims = parse_map(lines)
    antinodes = set()

    for c in freq_map:
        freq_set = freq_map[c]
        freqs = list(freq_set)

        for idx, f1 in enumerate(freqs[:-1]):
            for f2 in freqs[idx + 1:]:
                x1, y1 = f1
                x2, y2 = f2
                dx, dy = x2 - x1, y2 - y1

                antinodes.add(f1)
                antinodes.add(f2)


                while True:
                    a1 = x1 - dx, y1 - dy
                    x1, y1 = a1

                    if within_bounds(dims, a1) and a1 not in freqs:
                        antinodes.add(a1)
                    else:
                        break

                while True:
                    a2 = x2 + dx, y2 + dy
                    x2, y2 = a2

                    if within_bounds(dims, a2) and a2 not in freqs:
                        antinodes.add(a2)
                    else:
                        break

    print_map(dims, freq_map, antinodes)
    return len(antinodes)


def main():
    lines = sys.stdin.read().strip().split('\n')
    print("Part1: {}".format(part1(lines[:])))
    print("Part2: {}".format(part2(lines[:])))


if __name__ == "__main__":
    main()


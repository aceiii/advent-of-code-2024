#!/usr/bin/env python3

import sys
from enum import Enum


def parse_map(lines):
    height = len(lines)
    width = len(lines[0].strip())

    facing = None
    start_pos = None
    obstacles = []
    for y, line in enumerate(lines):
        for x, c in enumerate(line.strip()):
            pos = (x, y)
            if c == '#':
                obstacles.append(pos)
            elif c == '^':
                start_pos = pos
                facing = 0

    return (width, height), start_pos, facing, obstacles


def is_outside_map(dims, pos):
    w, h = dims
    x, y = pos
    return x < 0 or y < 0 or x >= w or y >= h


def next_positions(pos, facing):
    x, y = pos
    offsets = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    for idx in range(4):
        new_facing = (facing + idx) % 4
        dx, dy = offsets[new_facing]
        yield (x + dx, y + dy), new_facing


def get_next_pos(pos, facing, obstacles):
    for next_pos, new_facing in next_positions(pos, facing):
        if not (next_pos in obstacles):
            return next_pos, new_facing


def print_map(dims, pos, facing, obstacles):
    width, height = dims
    guard_map = ['^', '>', 'v', '<']
    for y in range(height):
        row = []
        for x in range(width):
            tile = (x, y)
            if tile == pos:
                row.append(guard_map[facing])
            elif tile in obstacles:
                row.append('#')
            else:
                row.append('.')
        print(''.join(row))
    print()


def part1(lines):
    dims, pos, facing, obstacles = parse_map(lines)
    steps = set()
    while not is_outside_map(dims, pos):
        steps.add(pos)
        pos, facing = get_next_pos(pos, facing, obstacles)
    return len(steps)


def part2(lines):
    pass


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


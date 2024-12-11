#!/usr/bin/env python3

import sys


def within_bounds(dims, pos):
    w, h = dims
    x, y = pos
    return x >= 0 and x < w and y >= 0 and y < h


def neighbour_tiles(pos):
    x, y = pos
    yield (x, y - 1)
    yield (x + 1, y)
    yield (x, y + 1)
    yield (x - 1, y)


def parse_map(lines):
    height_map = []
    for line in lines:
        if not line.strip():
            break

        row = []
        for c in line.strip():
            row.append(int(c, 10))
        height_map.append(row)

    height = len(height_map)
    width = len(height_map[0])
    dims = (width, height)

    trail_heads = []
    targets = []
    graph = {}

    for y, row in enumerate(height_map):
        for x, h in enumerate(row):
            pos = (x, y)

            if h == 0:
                trail_heads.append(pos)
            elif h == 9:
                targets.append(pos)

            next = [(nx, ny) for nx, ny in neighbour_tiles(pos) if within_bounds(dims,(nx, ny)) and height_map[ny][nx] == h + 1]
            graph[pos] = next

    return trail_heads, targets, height_map, graph, dims


def trail_score(trail_head, targets, height_map, graph, dims):
    target_set = set(targets)
    reached = set()
    stack = [trail_head]
    while stack:
        pos = stack.pop()
        if pos in target_set:
            reached.add(pos)
        for npos in graph[pos]:
            stack.append(npos)
    return len(reached)


def part1(lines):
    trail_heads, targets, height_map, graph, dims = parse_map(lines)
    return sum(trail_score(pos, targets, height_map, graph, dims) for pos in trail_heads)


def part2(lines):
    pass


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


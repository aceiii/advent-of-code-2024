#!/usr/bin/env python3

import sys
from operator import itemgetter


def within_bounds(pos, dims):
    x, y = pos
    w, h = dims
    return x >= 0 and x < w and y >= 0 and y < h


def neighbours(pos):
    x, y = pos
    yield (x, y-1)
    yield (x+1, y)
    yield (x, y+1)
    yield (x-1, y)


def count_groups(sides):
    sides = sides[:]
    reduced_sides = []
    while sides:
        side = sides.pop(0)
        if not reduced_sides:
            reduced_sides.append(side)
            continue

        prev_side = reduced_sides[-1]
        x, y, s = side
        px, py, ps = prev_side
        dx, dy = x - px, y - py

        if ps != s or dx > 0 or dy > 1:
            reduced_sides.append(side)
            continue

        reduced_sides.pop()
        reduced_sides.append(side)
    return len(reduced_sides)


def find_region(pos, grid, dims, visited):
    width, height = dims
    stack = [pos]
    perimeter = 0
    area = 0

    vert_sides = []
    hor_sides = []

    side_map = {
        (0, -1): ('-', (0, 0), 0),
        (1,  0): ('|', (1, 0), 0),
        (0,  1): ('-', (0, 1), 1),
        (-1, 0): ('|', (0, 0), 1),
    }

    while stack:
        pos = stack.pop()
        if pos in visited:
            continue

        visited.add(pos)
        x,y = pos
        tile = grid[y][x]
        area += 1
        perimeter += 4

        next = [(nx, ny) for nx, ny in neighbours(pos) if within_bounds((nx, ny), dims) and grid[ny][nx] == tile]
        perimeter -= len(next)
        for npos in next:
            stack.append(npos)

        sides = set(side_map.keys())
        for npos in neighbours(pos):
            if not within_bounds(npos, dims):
                continue

            nx, ny = npos
            if within_bounds(npos, dims) and grid[ny][nx] != tile:
                continue

            dpos = nx - x, ny - y
            sides.remove(dpos)

        for side in sides:
            sdir, (dx, dy), ss = side_map[side]
            spos = (x + dx, y + dy, ss)

            if sdir == '-':
                hor_sides.append(spos)
            else:
                vert_sides.append(spos)

    num_sides = count_groups(sorted(vert_sides)) + count_groups(sorted((y,x,s) for x,y,s in hor_sides))
    return (area, perimeter, num_sides)


def parse_map(lines):
    height = len(lines)
    width = len(lines[0])
    dims = width, height
    regions = []
    visited = set()
    
    grid = []
    for line in lines:
        row = []
        for tile in line:
            row.append(tile)
        grid.append(row)

    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            pos = (x, y)
            if pos in visited:
                continue
            regions.append(find_region(pos, grid, dims, visited))

    return regions


def part1(lines):
    regions = parse_map(lines)
    return sum(a * p for a, p, _ in regions)


def part2(lines):
    regions = parse_map(lines)
    return sum(a * s for a, p, s in regions)


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


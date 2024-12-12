#!/usr/bin/env python3

import sys


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


def find_region(pos, grid, dims, visited):
    stack = [pos]
    perimeter = 0
    area = 0

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

    return (area, perimeter)


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
    return sum(a * p for a, p in regions)


def part2(lines):
    pass


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


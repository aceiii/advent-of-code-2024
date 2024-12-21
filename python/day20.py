#!/usr/bin/env python3

import sys


def within_bounds(pos, dims):
    x, y = pos
    w, h = dims
    return x >= 0 and x < w and y >= 0 and y < h


def neighbours(pos):
    x, y = pos
    yield x + 1, y
    yield x, y + 1
    yield x - 1, y
    yield x, y - 1


def cheat_tiles(pos):
    x, y = pos
    yield [(x + 1, y), (x + 2, y)]
    yield [(x, y + 1), (x, y + 2)]
    yield [(x - 1, y), (x - 2, y)]
    yield [(x, y - 1), (x, y - 2)]


def parse_track(lines):
    height = len(lines)
    width = len(lines[0])
    dims = width, height

    start = None,
    end = None
    grid = []
    for y, line in enumerate(lines):
        row = []
        for x, c in enumerate(line):
            pos = x, y

            if c == "S":
                start = pos
            elif c == "E":
                end = pos

            row.append(False if c == "#" else True)
        grid.append(row)

    pos = start
    path = []
    while pos != end:
        for nx, ny in neighbours(pos):
            npos = nx,ny
            track = grid[ny][nx]
            if track and not (path and path[-1] == npos):
                path.append(pos)
                pos = npos
                break

    path.append(pos)
    dist = { p:d for d, p in enumerate(path) }
    return path, dist, grid, dims, start, end


def find_all_cheats(path, dist, grid, dims):
    cheats = []

    for pos in path:
        for apos, bpos in cheat_tiles(pos):
            ax, ay = apos
            bx, by = bpos

            if not within_bounds(apos, dims) or not within_bounds(bpos, dims):
                continue

            atrack = grid[ay][ax]
            btrack = grid[by][bx]

            if not atrack and btrack:
                cheat = pos, bpos
                end_dist= dist[bpos]
                start_dist = dist[pos]

                saved = end_dist - start_dist - 2
                if saved <= 0:
                    continue

                cheats.append((cheat, saved))
                continue


    return cheats


def find_all_cheats_max_n(path, dist, grid, dims, n):
    cheats = []

    for idx, pos in enumerate(path):
        x, y = pos
        for npos in path[idx + 1:]:
            nx, ny = npos
            dx, dy = nx - x, ny - y
            d = abs(dx) + abs(dy)

            if d > n:
                continue

            cheat = pos, npos
            end_dist = dist[npos]
            start_dist = dist[pos]
            saved = end_dist - start_dist - d
            if saved:
                cheats.append((cheat, saved))

    return cheats


def part1(lines):
    path, dist, grid, dims, start, end = parse_track(lines)
    cheats = find_all_cheats_max_n(path, dist, grid, dims, 2)

    count = 0
    for cheat, saved in cheats:
        if saved >= 100:
            count += 1

    return count


def part2(lines):
    path, dist, grid, dims, start, end = parse_track(lines)
    cheats = find_all_cheats_max_n(path, dist, grid, dims, 20)

    count = 0
    for cheat, saved in cheats:
        if saved >= 100:
            count += 1

    return count


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


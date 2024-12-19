#!/usr/bin/env python3

import sys
from operator import itemgetter


def within_bounds(pos, dims):
    x, y = pos
    w, h = dims
    return x >= 0 and x < w and y >= 0 and y < h


def neighbours(pos):
    x, y  = pos
    yield x + 1, y
    yield x, y + 1
    yield x - 1, y
    yield x, y - 1


def parse_map(lines):
    start = None
    end = None
    verts = set()
    edges = set()
    height = len(lines)
    width = len(lines[0])

    for y, line in enumerate(lines):
        for x, tile in enumerate(line):
            pos = x, y

            if tile == "#":
                continue
            elif tile == "S":
                start = pos
            elif tile == "E":
                end = pos

            verts.add(pos)

            if y - 1 >= 0 and lines[y-1][x] != "#":
                up = x, y-1
                edges.add((pos, up))
                edges.add((up, pos))

            if x - 1 >= 0 and lines[y][x-1] != "#":
                left = x-1, y
                edges.add((pos, left))
                edges.add((left, pos))

    return start, end, (verts, edges), (width, height)


def print_map(graph, dims):
    w, h = dims
    verts, edges = graph
    for y in range(h):
        row = []
        for x in range(w):
            pos = x, y
            row.append("." if pos in verts else "#")

        print("".join(row))
    print()


def print_map_path(graph, path, dims):
    w, h = dims
    verts, edges = graph

    for y in range(h):
        row = []
        for x in range(w):
            pos = x, y
            row.append("O" if pos in path else "." if pos in verts else "#")

        print("".join(row))
    print()


def part1(lines):
    start, end, graph, dims = parse_map(lines)
    verts, edges = graph

    up = (0, -1)
    right = (1, 0)
    left = (-1, 0)
    down = (0, 1)

    q = [(start, right, 0, {start: None})] 
    dist = {}

    while q:
        pos, dir, score, path = q.pop(0)

        if pos in dist and score > dist[pos]:
            continue

        dist[pos] = score

        new_nodes = []
        for npos in neighbours(pos):
            if not within_bounds(npos, dims):
                continue

            if npos in path:
                continue

            if (pos, npos) not in edges:
                continue

            new_path = path.copy()
            new_path[npos] = pos

            x,y = pos
            nx, ny = npos
            nd = nx - x, ny - y

            new_score = score + 1 + (0 if nd == dir else 1000)

            if npos in dist and new_score >= dist[npos]:
                continue

            new_nodes.append((npos, nd, new_score, new_path))

        new_nodes.sort(key=itemgetter(2))
        q.extend(new_nodes)

    return dist[end]


def part2(lines):
    start, end, graph, dims = parse_map(lines)
    verts, edges = graph

    up = (0, -1)
    right = (1, 0)
    left = (-1, 0)
    down = (0, 1)

    dist = {}
    paths = []
    q = [(start, right, 0, {start: None})] 

    while q:
        pos, dir, score, path = q.pop()

        if (pos,dir) in dist and score > dist[(pos,dir)]:
            continue

        if pos == end:
            paths.append((score, path))

        dist[(pos,dir)] = score

        new_nodes = []
        for npos in neighbours(pos):
            if not within_bounds(npos, dims):
                continue

            if npos in path:
                continue

            if (pos, npos) not in edges:
                continue

            new_path = path.copy()
            new_path[npos] = pos

            x,y = pos
            nx, ny = npos
            nd = nx - x, ny - y

            new_score = score + 1 + (0 if nd == dir else 1000)

            new_nodes.append((npos, nd, new_score, new_path))

        new_nodes.sort(key=itemgetter(2), reverse=True)
        q.extend(new_nodes)


    paths.sort(key=itemgetter(0))

    tiles = set()
    cs = float("inf")
    for s, p in paths:
        if s <= cs:
            tiles.update(p)
            cs = s

    #print_map_path(graph, tiles, dims)
    return len(tiles)


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


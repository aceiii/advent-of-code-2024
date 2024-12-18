#!/usr/bin/env python3

import sys
from heapq import heapify, heappush, heappop


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


def build_graph(dims, blocked):
    w, h = dims
    verts = []
    edges = set()

    for y in range(h):
        for x in range(w):
            pos = x, y
            if pos in blocked:
                continue

            verts.append(pos)

            for npos in neighbours(pos):
                if not within_bounds(npos, dims):
                    continue

                if npos in blocked:
                    continue

                edges.add((pos, npos))
                edges.add((npos, pos))

    return verts, edges


def dijkstra(graph, start):
    verts, edges = graph
    dist = {}
    prev = {}
    q = []

    for v in verts:
        dist[v] = float("inf")
        prev[v] = None
        q.append(v)

    dist[start] = 0

    while q:
        q.sort(key=lambda x: dist[x], reverse=True)
        u = q.pop()

        for v in neighbours(u):
            if (v,u) not in edges or v not in q:
                continue

            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

    return dist, prev



def part1(lines):
    dims = 71, 71
    n = 1024

    """
    dims = 7, 7
    n = 12
    """

    falling = [tuple(int(a, 10) for a in line.split(',')) for line in lines]
    fallen = set(falling[:n])

    graph = build_graph(dims, fallen)
    dist, prev = dijkstra(graph, (0, 0))
    end = dims[0]-1, dims[1] -1

    return dist[end]


def part2(lines):
    pass


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


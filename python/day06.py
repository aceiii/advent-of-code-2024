#!/usr/bin/env python3

import sys
from enum import Enum
from collections import defaultdict


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



def positions_between(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    dx = x2 - x1
    dy = y2 - y1

    if dx != 0:
        for nx in range(x1 + 1, x2 - 1, int(dx/abs(dx))):
            yield (nx, y1)
    elif dy != 0:
        for ny in range(y1 + 1, y2 - 1, int(dy/abs(dy))):
            yield (x1, ny)


def find_intersecting_guard_point(guard_points_by_x, guard_points_by_y, pos, facing, dims, obstacles):
    x, y = pos
    if facing == 0:
        for gp in guard_points_by_y[y]:
            gx, gy = gp
            if gx <= x:
                continue
            if all(np not in obstacles for np in positions_between(pos, gp)):
                print("found",pos,facing, gp)
                return True
    elif facing == 1:
        for gp in guard_points_by_x[x]:
            gx, gy = gp
            if gy <= y:
                continue
            if all(np not in obstacles for np in positions_between(pos, gp)):
                print("found", pos, facing, gp)
                return True
    elif facing == 2:
        for gp in guard_points_by_y[y]:
            gx, gy = gp
            if gx >= x:
                continue
            if all(np not in obstacles for np in positions_between(pos, gp)):
                print("found", pos, facing, gp)
                return True
    elif facing == 3:
        for gp in guard_points_by_x[x]:
            gx, gy = gp
            if gy >= y:
                continue
            if all(np not in obstacles for np in positions_between(pos, gp)):
                print("found", pos, facing, gp)
                return True
    return False


def has_loop(graph, start):
    current = start
    while current:
        current = graph[current]
        if current == start:
            return True
    return False
        

def part2_test(lines):
    dims, start_pos, start_facing, obstacles = parse_map(lines)
    obstacles = set(obstacles)
    width, height = dims
    answer = 0
    for y in range(height):
        for x in range(width):
            block = (x, y)
            if block in obstacles:
                continue

            obstacles.add(block)
            prev_intersection = None
            intersection_graph = {}

            pos, facing = start_pos, start_facing
            while not is_outside_map(dims, pos):
                new_pos, new_facing = get_next_pos(pos, facing, obstacles)
                if new_facing != facing:
                    intersection_graph[pos] = prev_intersection
                    if has_loop(intersection_graph, pos):
                        answer += 1
                        break
                    prev_intersection = pos

                pos, facing = new_pos, new_facing

            obstacles.remove(block)
            

    return answer


def part2(lines):
    dims, pos, facing, obstacles = parse_map(lines)
    guard_path = []
    guard_points_by_x = defaultdict(lambda: set())
    guard_points_by_y = defaultdict(lambda: set())

    answer = 0
    while not is_outside_map(dims, pos):
        if find_intersecting_guard_point(guard_points_by_x, guard_points_by_y, pos, facing, dims, obstacles):
            answer += 1

        new_pos, new_facing = get_next_pos(pos, facing, obstacles)
        if new_facing != facing:
            x, y = pos
            guard_path.append(pos)
            guard_points_by_x[x].add(pos)
            guard_points_by_y[y].add(pos)
            
        facing = new_facing
        pos = new_pos
    return answer


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


#!/usr/bin/env python3

import sys


class WarehouseTile:
    def __init__(self, pos, type_):
        self.pos = pos
        self.type = type_
        self.right = None
        self.left = None
        self.up = None
        self.down = None

    def next(self, m):
        if m == "^":
            return self.up
        elif m == ">":
            return self.right
        elif m == "<":
            return self.left
        else:
            return self.down

    def __repr__(self):
        return f"WhTile({self.pos}: {self.type})"


class Warehouse:
    def __init__(self, lines):
        self.height = len(lines)
        self.width = len(lines[0])

        tile_map = {}
        self.grid = []

        for y, line in enumerate(lines):
            row = []
            for x, tile in enumerate(line):
                pos = x, y

                if tile == "@":
                    self.robot = pos

                moveable = tile != "#"
                empty = tile == "." or tile == "@"

                tile_type = 0
                if tile == "O":
                    tile_type = 1
                elif tile == "#":
                    tile_type = 2

                wh_tile = WarehouseTile(pos, tile_type)
                tile_map[pos] = wh_tile

                up = (x, y-1)
                left = (x-1, y)

                if left in tile_map:
                    left_tile = tile_map[left]
                    left_tile.right = wh_tile
                    wh_tile.left = left_tile

                if up in tile_map:
                    up_tile = tile_map[up]
                    up_tile.down = wh_tile
                    wh_tile.up = up_tile

                row.append(wh_tile) 
            self.grid.append(row)

    def tile_at(self, pos):
        x, y = pos
        return self.grid[y][x]


    def __repr__(self):
        return f"Warehouse({self.width}, {self.height})"


    def print_map(self):
        for y, row in enumerate(self.grid):

            line = []
            for x, tile in enumerate(row):
                pos = x, y

                if pos == self.robot:
                    line.append("@")

                elif tile.type == 0:
                    line.append(".")
                elif tile.type == 1:
                    line.append("O")
                else:
                    line.append("#")

            print("".join(line))
        print()

    def move(self, m):
        moves = {
            "^": (0, -1),
            "<": (-1, 0),
            ">": (1, 0),
            "v": (0, 1),
        }

        x, y = self.robot
        dx, dy = moves[m]
        new_pos = x + dx, y + dy

        tile = self.tile_at(new_pos)
        first = tile

        while tile.type == 1:
            tile = tile.next(m)

        if tile.type == 0:
            self.robot = new_pos

            tile.type = first.type
            first.type = 0

    def gps_score(self):
        score = 0
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                if tile.type == 1:
                    score += 100 * y + x
        return score


def parse_warehouse(lines):
    lines = lines[:]

    wh_lines = []
    moves = []

    map_mode = True
    while lines:
        line = lines.pop(0).strip()

        if not line:
            map_mode = False
            continue

        if map_mode:
            wh_lines.append(line)
        else:
            moves.extend(c for c in line)

    warehouse = Warehouse(wh_lines)
    return warehouse, moves


def part1(lines):
    wh, moves = parse_warehouse(lines)
    #wh.print_map()

    for m in moves:
        wh.move(m)
        # wh.print_map()

    return wh.gps_score()


def part2(lines):
    pass


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


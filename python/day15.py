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


class WideBlock:
    def __init__(self, pos, moveable):
        x, y = pos
        self._pos = set([(x, y), (x+1, y)])
        self.moveable = moveable

    def _add_pos(self, pos):
        self._pos.add(pos)

    def _remove_pos(self, pos):
        if pos in self._pos:
            self._pos.remove(pos)

    def pos(self):
        return sorted(self._pos)[0]

    def __repr__(self):
        return f"WideBlock({self.pos()})"


class WideWarehouse:
    def __init__(self, lines):
        self.height = len(lines)
        self.width = len(lines[0]) * 2

        self.grid = []
        self.blocks = []
        for y, line in enumerate(lines):
            row = []
            for x, tile in enumerate(line):
                pos = x * 2, y

                if tile == "@":
                    self.robot = pos

                block = None
                if tile == "#" or tile == "O":
                    block = WideBlock(pos, tile == "O")

                row.append(block)
                row.append(block)

                if block is not None:
                    self.blocks.append(block)
            self.grid.append(row)

    def __repr__(self):
        return f"WideWarehouse({self.width}, {self.height})"

    def print_map(self):
        for y, row in enumerate(self.grid):

            line = []
            for x, tile in enumerate(row):
                pos = x, y

                if pos == self.robot:
                    line.append("@")
                elif tile is None:
                    line.append(".")
                elif tile.moveable == False:
                    line.append("#")
                else:
                    tx,ty = tile.pos()
                    dx = tx - x
                    if dx == 0:
                        line.append("[")
                    else:
                        line.append("]")

            print("".join(line))
        print()

    def tile_at(self, pos):
        x, y = pos
        return self.grid[y][x]

    def set_tile_at(self, pos, tile):
        x, y = pos
        self.grid[y][x] = tile

    def move_hor(self, dx):
        x, y = self.robot
        mx = 0
        while True:
            x += dx
            mx += 1
            tile = self.tile_at((x, y))
            if tile is None:
                break
            if not tile.moveable:
                return

        x, y = self.robot
        cx = x + (mx * dx)

        while mx > 1:
            p1 = (cx, y)
            p2 = (cx - dx, y)

            t1 = self.tile_at(p1)
            t2 = self.tile_at(p2)

            self.set_tile_at(p1, t2)
            self.set_tile_at(p2, t1)

            if t1:
                t1._remove_pos(p1)
                t1._add_pos(p2)

            if t2:
                t2._remove_pos(p2)
                t2._add_pos(p1)

            cx += -dx
            mx -= 1

        if mx:
            self.robot = (x + dx, y)

    def move_vert(self, dy):
        x, y = self.robot
        stack = [(x, y + dy)]
        visited = set()
        to_move = []
        while stack:
            pos = stack.pop()
            tile = self.tile_at(pos)

            if tile is None:
                continue

            if tile in visited:
                continue

            if not tile.moveable:
                return

            visited.add(tile)
            to_move.append(tile)

            tx, ty = tile.pos()
            stack.append((tx, ty + dy))
            stack.append((tx + 1, ty + dy))

        to_move.sort(key=lambda b: (b.pos()[1] * dy, b.pos()[0]))

        while to_move:
            tile = to_move.pop()
            tx, ty = tile.pos()

            p1 = (tx, ty)
            p2 = (tx + 1, ty)
            p3 = (tx, ty + dy)
            p4 = (tx + 1, ty + dy)

            tile._remove_pos(p1)
            tile._remove_pos(p2)
            tile._add_pos(p3)
            tile._add_pos(p4)

            self.set_tile_at(p1, None)
            self.set_tile_at(p2, None)
            self.set_tile_at(p3, tile)
            self.set_tile_at(p4, tile)

        self.robot = (x, y + dy)

    def move(self, m):
        moves = {
            "^": (0, -1),
            "<": (-1, 0),
            ">": (1, 0),
            "v": (0, 1),
        }

        dx, dy = moves[m]
        if dx != 0:
            self.move_hor(dx)
        else:
            self.move_vert(dy)

    def gps_score(self):
        score = 0
        for block in self.blocks:
            if block.moveable:
                x,y = block.pos()
                score += (y * 100) + x
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

    return wh_lines, moves


def part1(lines):
    wh_lines, moves = parse_warehouse(lines)
    wh = Warehouse(wh_lines)
    #wh.print_map()

    for m in moves:
        wh.move(m)
        #wh.print_map()

    return wh.gps_score()


def part2(lines):
    wh_lines, moves = parse_warehouse(lines)
    wh = WideWarehouse(wh_lines)
    #wh.print_map()

    print(len(moves))
    n = 0
    for m in moves:
        wh.move(m)
        #wh.print_map()

        n += 1
        #if n == 3500:
        #    break

    wh.print_map()
    return wh.gps_score()


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


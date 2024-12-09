#!/usr/bin/env python3

import sys


def parse_disk(line):
    idx = 0
    blocks = []
    while idx < len(line):
        file = int(line[idx:idx+1], 10)
        free = int(line[idx+1:idx+2] or '0', 10)
        blocks.append((file, free))
        idx += 2
    return blocks


def calc_checksum(blocks):
    result = 0
    idx = 0
    for _, len, multiplier in blocks:
        ans = multiplier * sum(range(idx, idx + len))
        idx += len
        result += ans
    return result


def print_blocks(blocks):
    print(''.join(''.join([str('.' if c is None else c)]*n) for _, n, c in sorted(blocks)))


def part1(lines):
    blocks = parse_disk(lines[0])

    free_blocks = []
    used_blocks = []

    block_idx = 0
    for idx, (file, free) in enumerate(blocks):
        used_blocks.append((block_idx, file, idx))
        block_idx += file

        if free:
            free_blocks.append((block_idx, free, None))
            block_idx += free

    moved_blocks = []

    while free_blocks:
        free_block_idx, free_len, _ = free_blocks.pop(0)

        while free_len > 0:
            used_block_idx, block_len, block_id = used_blocks.pop()
            if free_block_idx > used_block_idx:
                used_blocks.append((used_block_idx, block_len, block_id))
                break

            new_used_len = min(block_len, free_len)
            moved_blocks.append((free_block_idx, new_used_len, block_id))
            if block_len > free_len:
                used_blocks.append((block_idx, block_len - free_len, block_id))
            free_len -= block_len
            free_block_idx += block_len

    return calc_checksum(sorted(used_blocks + moved_blocks))


def part2(lines):
    pass


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines[:])))
    print("Part2: {}".format(part2(lines[:])))


if __name__ == "__main__":
    main()


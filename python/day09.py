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
    for start_idx, len, multiplier in blocks:
        ans = (0 if multiplier is None else multiplier) * sum(range(idx, idx  + len))
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


def compact_free_blocks(blocks):
    free_blocks = []

    for block in blocks:
        block_idx, block_len, _ = block
        if free_blocks and free_blocks[-1][0] + free_blocks[-1][1] == block_idx:
            prev_block_idx, prev_block_len, _ = free_blocks[-1]
            free_blocks[-1] = (prev_block_idx, prev_block_len + block_len, None)
            continue

        free_blocks.append(block)

    return free_blocks

def part2(lines):
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

    while used_blocks:
        used_block_idx, block_len, block_id = used_blocks.pop()

        for i in range(len(free_blocks)):
            if free_blocks[i][1] < block_len:
                continue

            free_block_idx, free_len, _ = free_blocks.pop(i)
            if free_block_idx >= used_block_idx:
                free_blocks.insert(i, (free_block_idx, free_len, None))
                moved_blocks.append((used_block_idx, block_len, block_id))
                break

            moved_blocks.append((free_block_idx, block_len, block_id))
            free_blocks.append((used_block_idx, block_len, None))

            if free_len > block_len:
                free_blocks.append((free_block_idx + block_len, free_len - block_len, None))
                free_blocks.sort()

            break

        else:
            moved_blocks.append((used_block_idx, block_len, block_id))

        free_blocks = compact_free_blocks(free_blocks)

    return calc_checksum(sorted(used_blocks + moved_blocks + free_blocks))

def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines[:])))
    print("Part2: {}".format(part2(lines[:])))


if __name__ == "__main__":
    main()


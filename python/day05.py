#!/usr/bin/env python3

import sys
from collections import defaultdict


def gen_idx_map(line):
    idx_map = defaultdict(lambda: None)
    for idx, n in enumerate(line):
        idx_map[n] = idx
    return idx_map


def is_valid_line(line, idx_map, rule_map):
    for idx, n in enumerate(line):
        if not all(idx < idx_map[nn] for nn in rule_map[n] if idx_map[nn] is not None):
            return False
    
    return True

def mid_elem(elems):
    n = len(elems)
    return elems[int(n/2)]


def part1(lines):
    lines = lines[:]
    rule_map = defaultdict(lambda: set())
    rule_index_map = defaultdict(lambda: 0)
    while lines:
        line = lines.pop(0).strip()
        if not line.strip():
            break
        first, second = line.split("|")
        rule_map[int(first, 10)].add(int(second, 10))

    valid = []
    while lines:
        line = [int(n, 10) for n in lines.pop(0).strip().split(",")]
        idx_map = gen_idx_map(line)
        if is_valid_line(line, idx_map, rule_map):
            valid.append(line)

    return sum(mid_elem(line) for line in valid)


def fix_line(line, rule_map):
    idx_map = gen_idx_map(line)

    idx = 0
    while idx < len(line):
        n = line[idx]
        nidx = sorted(idx_map[nn] for nn in rule_map[n] if idx_map[nn] is not None)
        if all(idx < idx2 for idx2 in nidx):
            idx += 1
        else:
            idx2 = list(nidx)[0]
            nn = line[idx2]
            line[idx] = nn
            line[idx2] = n
            idx_map[nn] = idx
            idx_map[n] = idx2

    return line


def fix_lines(lines, rule_map):
    return [fix_line(line, rule_map) for line in lines]


def part2(lines):
    lines = lines[:]
    rule_map = defaultdict(lambda: set())
    rule_index_map = defaultdict(lambda: 0)
    while lines:
        line = lines.pop(0).strip()
        if not line.strip():
            break
        first, second = line.split("|")
        rule_map[int(first, 10)].add(int(second, 10))

    invalid = []
    while lines:
        line = [int(n, 10) for n in lines.pop(0).strip().split(",")]
        idx_map = gen_idx_map(line)
        if not is_valid_line(line, idx_map, rule_map):
            invalid.append(line)

    return sum(mid_elem(line) for line in fix_lines(invalid, rule_map))


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


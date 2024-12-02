#!/usr/bin/env python3

import sys



def same_dir(levels):
    return all(x < 0 for x in levels) or all(x > 0 for x in levels)


def safe_levels(levels):
    return all(abs(x) >= 1 and abs(x) <= 3 for x in levels)


def is_safe(levels):
    return same_dir(levels) and safe_levels(levels)


def fix_levels(levels):
    pos = []
    neg = []
    zero = []
    over = []
    for idx, level in enumerate(levels):
        if abs(level) > 3:
            over.append(idx)

        if level < 0:
            neg.append(idx)
        elif level > 0:
            pos.append(idx)
        else:
            zero.append(idx)

    zeroes = len(zero)
    poses = len(pos)
    negs = len(neg)

    if zeroes > 1:
        return False

    if poses > 1 and negs > 1:
        return False


    if zeroes == 1:
        new_levels = levels[:]
        new_levels.pop(zero[0])
        return same_dir(new_levels) and safe_levels(new_levels)

    idx = None
    if negs == 1:
        idx = neg[0]
    elif poses == 1:
        idx = pos[0]
    else:
        if len(over) > 1:
            return False
        idx = over[0]


    levels2 = levels[:]
    if idx - 1 >= 0:
        levels2[idx-1] += levels2[idx]

    levels3 = levels[:]
    if idx + 1 < len(levels3):
        levels3[idx + 1] += levels3[idx]

    levels2.pop(idx)
    levels3.pop(idx)

    return is_safe(levels2) or is_safe(levels3)


def part1(lines):
    answer = 0
    for line in lines:
        if not line.strip():
            break
        levels = [int(n, 10) for n in line.split(" ")]
        diffs = []
        for i in range(len(levels) - 1):
            a, b = levels[i:i+2]
            diffs.append(b - a)

        if same_dir(diffs) and safe_levels(diffs):
            answer += 1
    return answer


def part2(lines):
    answer = 0
    for line in lines:
        if not line.strip():
            break
        levels = [int(n, 10) for n in line.split(" ")]
        diffs = []
        for i in range(len(levels) - 1):
            a, b = levels[i:i+2]
            diffs.append(b - a)

        if same_dir(diffs) and safe_levels(diffs):
            answer += 1
            continue

        if fix_levels(diffs):
            answer += 1
    return answer
    


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


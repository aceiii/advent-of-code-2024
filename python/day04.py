#!/usr/bin/env python3

import sys


def char_at(lines, pos):
    try:
        x, y = pos
        return lines[y][x]
    except:
        return ""


def diag_words(lines, pos, n):
    x, y = pos
    words = []
    words.append("".join(char_at(lines, (x+i, y+i)) for i in range(n)))
    words.append("".join(char_at(lines, (x-i, y+i)) for i in range(n)))
    return words    


def search_line(line, word):
    result = len(re.findall(word, line))
    return result + len(re.findall(word[::-1], line))


def search_horizontal(lines, pos, word):
    x, y = pos
    n = len(word)
    rword = word[::-1]
    line = lines[y]
    text = line[x:x+n]
    return 1 if text == word or text == rword else 0


def search_vertical(lines, pos, word):
    x, y = pos
    n = len(word)
    rword = word[::-1]
    text = "".join(char_at(lines, (x, y+i)) for i in range(n))
    return 1 if text == word or text == rword else 0


def search_diagonal(lines, pos, word):
    x, y = pos
    n = len(word)
    rword = word[::-1]
    result = 0
    for diag in diag_words(lines, pos, n):
        if diag == word or diag == rword:
            result += 1
    return result


def part1(lines):
    find = "XMAS"
    hors = 0
    diags = 0
    verts = 0
    for y, line in enumerate(lines):
        for x in range(len(line)):
            pos = x, y
            hors += search_horizontal(lines, pos, find)
            diags += search_diagonal(lines, pos, find)
            verts += search_vertical(lines, pos, find)
    return diags + hors + verts


def cross_words_at(lines, pos):
    x, y = pos
    word1 = "".join([
        char_at(lines, pos),
        char_at(lines, (x + 1, y + 1)),
        char_at(lines, (x + 2, y + 2)),
    ])
    word2 = "".join([
        char_at(lines, (x + 2, y)),
        char_at(lines, (x + 1, y + 1)),
        char_at(lines, (x, y + 2))
    ])
    return [word1, word2]


def part2(lines):
    answer = 0
    find = "MAS"
    rfind = find[::-1]
    for y, line in enumerate(lines):
        for x in range(len(line)):
            pos = x, y
            if all(w == find or w == rfind for w in cross_words_at(lines, pos)):
                answer += 1
    return answer


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


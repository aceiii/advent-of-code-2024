#!/usr/bin/env python3

import sys
from collections import defaultdict
from operator import itemgetter
from itertools import combinations



def parse_links(lines):
    nodes = set()
    links = set()

    for line in lines:
        a, b = line.split("-")
        nodes.add(a)
        nodes.add(b)
        links.add((a, b))
        links.add((b, a))

    return nodes, links


def find_connected_nodes(nodes, links):
    connected = []
    for a, b, c in combinations(nodes, 3):
        d = (a, b)
        e = (b, c)
        f = (c, a)
        if d in links and e in links and f in links:
            connected.append((a, b, c))
    return connected


def part1(lines):
    nodes, links = parse_links(lines)
    connected = find_connected_nodes(nodes, links)

    count = 0
    for conn in connected:
        for node in conn:
            if node[0] == "t":
                count += 1
                break
    return count


def connected_to_all_in_group(group, link, links):
    a, b = link
    for node in group:
        if (a, node) not in links or (b, node) not in links:
            return False
    return True


def find_largest_connected_set(nodes, links):
    links = links.copy()
    for node in nodes:
        links.add((node, node))

    groups = []
    visited = set()
    for link in links:
        link = tuple(sorted(link))
        if link in visited:
            continue

        visited.add(link)
        for group in groups:
            if connected_to_all_in_group(group, link, links):
                a, b = link
                group.add(a)
                group.add(b)

        groups.append(set(link))

    groups.sort(key=lambda a: len(a), reverse=True)
    return list(sorted(groups[0]))


def part2(lines):
    nodes, links = parse_links(lines)
    largest = find_largest_connected_set(nodes, links)
    return ",".join(largest)


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


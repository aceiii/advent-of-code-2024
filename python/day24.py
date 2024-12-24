#!/usr/bin/env python3

import sys
from collections import defaultdict


OP_MAP = {
    "AND": lambda a, b: a & b,
    "OR": lambda a, b: a | b,
    "XOR": lambda a, b: a ^ b,
}


def parse_wires(lines):
    vars = {}
    ops = []
    mode = 0
    for line in lines:
        line = line.strip()
        if not line.strip():
            mode = 1
            continue

        if mode == 0:
            name, val = line.split(": ")
            vars[name] = int(val, 10)
        else:
            first, target = line.split(" -> ")
            a, op, b = first.split(" ")
            ops.append((OP_MAP[op], a, b, target))
    return vars, ops


class Signals:
    def __init__(self):
        self._vals = defaultdict(lambda: None)
        self._listeners = defaultdict(lambda: set())

    def _trigger_ops(self, name):
        to_remove = []
        for listener in self._listeners[name]:
            removed = listener()

            if removed is None:
                continue

            for var in removed:
                to_remove.append((var, listener))

        for var, listener in to_remove:
            self._listeners[var].remove(listener)

    def set_var(self, name, val):
        self._vals[name] = val
        self._trigger_ops(name)

    def set_op(self, op, input_a, input_b, target):
        a = self.get(input_a)
        b = self.get(input_b)

        if a is not None and b is not None:
            self.set_var(target, op(a, b))
            return

        def callback():
            a = self.get(input_a)
            b = self.get(input_b)

            if a is None or b is None:
                return None

            self.set_var(target, op(a, b))
            return (input_a, input_b)

        if a is None:
            self._listeners[input_a].add(callback)

        if b is None:
            self._listeners[input_b].add(callback)

    def wires(self):
        return self._vals.items()

    def get(self, name):
        return self._vals[name]
    

def part1(lines):
    vars, ops = parse_wires(lines)
    signals = Signals()

    for op, a, b, target in ops:
        signals.set_op(op, a, b, target)

    for var, val in vars.items():
        signals.set_var(var, val)

    zwires = sorted([(k,str(v)) for k,v in signals.wires() if k[0] == "z"], reverse=True)
    val = "".join(v for _, v in zwires)
    return int(val, 2)

def part2(lines):
    pass


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


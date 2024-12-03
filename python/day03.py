#!/usr/bin/env python3

import sys
import string
import re


def is_digit(c):
    return c in string.digits


class Parser:
    def __init__(self, lines):
        self._lines = lines
        self._ops =  []
        for line in self._lines:
            self._line = line
            self._ops.extend(self.parse())

    def parse(self):
        ops = []
        self._idx = 0

        while self._idx < len(self._line):
            op = self.next_op()
            if op:
                ops.append(op)

        return ops

    def peek(self, n=0):
        idx = self._idx + n
        if idx >= len(self._line):
            return None
        return self._line[idx]

    def match(self, expected):
        n = len(expected)
        token = self._line[self._idx:self._idx+n]
        if token == expected:
            self._idx += n
            return True
        self._idx += 1
        return False

    def num(self):
        c = self.peek(0)
        self._idx += 1

        if not is_digit(c):
            return None

        digits = [c]
        while True:
            c = self.peek(0)
            if is_digit(c):
                digits.append(c)
                self._idx += 1
            else:
                break

        return "".join(digits)

    def mul(self):
        if not self.match("mul("):
            return None

        a = self.num()
        if a is None:
            return None

        if not self.match(","):
            return None

        b = self.num()
        if b is None:
            return None

        if not self.match(")"):
            return None

        return ("mul", (int(a, 10), int(b, 10)))

    def next_op(self):
        c = self.peek(0)
        if c == "m":
            return self.mul()
        elif c == "d":
            if self.match("don't()"):
                return ("dont",())

            self._idx -= 1
            if self.match("do()"):
                return ("do", ())

        else:
            self._idx += 1

        return None

    def ops(self):
        return self._ops


def part1(lines):
    parser = Parser(lines)
    ops = parser.ops()
    muls = (params for op, params in ops if op == "mul")
    return sum(a * b for a, b in muls)


def part2(lines):
    parser = Parser(lines)
    ops = parser.ops()

    enabled = True
    answer = 0
    while ops:
        op, params = ops.pop(0)
        if op == "mul" and enabled:
            a, b = params
            answer +=  a * b
        elif op == "do":
            enabled = True
        elif op == "dont":
            enabled = False
    return answer



def test(lines):
    ops = []
    for line in lines:
        ops.extend(re.findall(r"(mul)\((\d+),(\d+)\)|(do)\(\)|(don\'t)\(\)", line))

    answer = 0
    enabled = True
    for mul, a, b, do, dont in ops:
        if mul and enabled:
            answer += int(a, 10) * int(b, 10)
        elif do:
            enabled = True
        elif dont:
            enabled = False
    print(answer)


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


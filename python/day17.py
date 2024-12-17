#!/usr/bin/env python3

import sys



def combo_operand(operand):
    if operand == 4:
        return "A"
    elif operand == 5:
        return "B"
    elif operand == 6:
        return "C"
    else:
        return operand


def parse_operands(op, operand):
    if op == 0:
        return combo_operand(operand)
    elif op == 1:
        return operand
    elif op == 2:
        return combo_operand(operand)
    elif op == 3:
        return operand
    elif op == 4:
        return operand
    elif op == 5:
        return combo_operand(operand)
    elif op == 6:
        return combo_operand(operand)
    elif op == 7:
        return combo_operand(operand)


def parse_program(lines):
    registers = {}
    instructions = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line[:8] == "Register":
            name, val = line[9:].split(": ")
            registers[name] = int(val, 10)
        else:
            instructions = [int(x, 10) for x in line[9:].split(",")]


    program = []
    for i in range(0, len(instructions), 2):
        op = instructions[i]
        operand = instructions[i+1]
        program.append((op, parse_operands(op, operand)))

    return program, registers


def step_program(instruction, registers, ip):
    op, operand = instruction
    val = registers[operand] if type(operand) == str else operand
    out = None

    if op == 0:
        num = registers["A"]
        den = 2**val
        registers["A"] = num // den

    elif op == 1:
        registers["B"] ^= val

    elif op == 2:
        registers["B"] = val % 8
    
    elif op == 3:
        if registers["A"]:
            return val, None

    elif op == 4:
        registers["B"] ^= registers["C"]

    elif op == 5:
        out = val % 8

    elif op == 6:
        num = registers["A"]
        den = 2**val
        registers["B"] = num // den

    elif op == 7:
        num = registers["A"]
        den = 2**val
        registers["C"] = num // den

    return ip + 2, out


def run_program(program, registers):
    n = len(program) * 2
    ip = 0
    output = []

    while ip < n:
        instruction = program[ip // 2]
        next_ip, out = step_program(instruction, registers, ip)
        if out is not None:
            output.append(out)
        ip = next_ip

    return output


def part1(lines):
    program, registers = parse_program(lines)
    output = run_program(program, registers)
    return ",".join(map(str, output))

def part2(lines):
    pass


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


from collections import Counter, defaultdict
from pprint import pprint


def addr(registers, a, b, c):
    """(add register) stores into register C the result of adding register A and register B."""
    registers[c] = registers[a] + registers[b]
    return registers


def addi(registers, a, b, c):
    """(add immediate) stores into register C the result of adding register A and value B."""
    registers[c] = registers[a] + b
    return registers


def mulr(registers, a, b, c):
    """(multiply register) stores into register C the result of multiplying register A and register B."""
    registers[c] = registers[a] * registers[b]
    return registers


def muli(registers, a, b, c):
    """(multiply immediate) stores into register C the result of multiplying register A and value B."""
    registers[c] = registers[a] * b
    return registers


def banr(registers, a, b, c):
    """(bitwise AND register) stores into register C the result of the bitwise AND of register A and register B."""
    registers[c] = registers[a] & registers[b]
    return registers


def bani(registers, a, b, c):
    """(bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B."""
    registers[c] = registers[a] & b
    return registers


def borr(registers, a, b, c):
    """(bitwise OR register) stores into register C the result of the bitwise OR of register A and register B."""
    registers[c] = registers[a] | registers[b]
    return registers


def bori(registers, a, b, c):
    """(bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B."""
    registers[c] = registers[a] | b
    return registers


def setr(registers, a, b, c):
    """(set register) copies the contents of register A into register C. (Input B is ignored.)"""
    registers[c] = registers[a]
    return registers


def seti(registers, a, b, c):
    """(set immediate) stores value A into register C. (Input B is ignored.)"""
    registers[c] = a
    return registers


def gtir(registers, a, b, c):
    """(greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0."""
    registers[c] = int(a > registers[b])
    return registers


def gtri(registers, a, b, c):
    """(greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0."""
    registers[c] = int(registers[a] > b)
    return registers


def gtrr(registers, a, b, c):
    """(greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0."""
    registers[c] = int(registers[a] > registers[b])
    return registers


def eqir(registers, a, b, c):
    """(equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0."""
    registers[c] = int(a == registers[b])
    return registers


def eqri(registers, a, b, c):
    """(equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0."""
    registers[c] = int(registers[a] == b)
    return registers


def eqrr(registers, a, b, c):
    """(equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0."""
    registers[c] = int(registers[a] == registers[b])
    return registers


INSTRUCTIONS = {
    addr,
    addi,
    mulr,
    muli,
    banr,
    bani,
    borr,
    bori,
    setr,
    seti,
    gtir,
    gtri,
    gtrr,
    eqir,
    eqri,
    eqrr,
}


def parse_puzzle(puzzle_input_file):
    samples = []
    program = []
    with open(puzzle_input_file, "r") as puzzle_input:
        blank_count = 0
        for line in puzzle_input:
            line = line.strip()
            if line.startswith("Before:"):
                blank_count = 0
                before = eval(line.split(":")[1])
            elif line.startswith("After:"):
                after = eval(line.split(":")[1])
                samples.append((before, statement, after))
            elif not line:
                blank_count += 1
            else:
                statement = tuple(int(x) for x in line.split())
                if blank_count > 2:
                    program.append(statement)
    return samples, program


def count_ambiguous_inputs(puzzle_input_file, limit=3):
    total = 0
    for before, (_, a, b, c), after in parse_puzzle(puzzle_input_file)[0]:
        match_count = sum(
            int(func(before[:], a, b, c) == after) for func in INSTRUCTIONS
        )
        if match_count > limit:
            total += 1
    return total


def run_puzzle_program(puzzle_input_file):
    samples, program = parse_puzzle(puzzle_input_file)
    # Infer opcodes
    codes_to_possibilities = defaultdict(set)
    codes_to_funcs = {}
    funcs_to_codes = {}
    for before, (opcode, a, b, c), after in samples:
        if opcode in codes_to_funcs:
            continue
        possible_matches = {
            func
            for func in INSTRUCTIONS
            if func not in funcs_to_codes and func(before[:], a, b, c) == after
        }
        if opcode in codes_to_possibilities:
            codes_to_possibilities[opcode] = codes_to_possibilities[
                opcode
            ].intersection(possible_matches)
        else:
            codes_to_possibilities[opcode] = possible_matches
        if len(codes_to_possibilities[opcode]) == 1:
            func = next(iter(codes_to_possibilities[opcode]))
            codes_to_funcs[opcode] = func
            funcs_to_codes[func] = opcode
            del codes_to_possibilities[opcode]
            for poss_set in codes_to_possibilities.values():
                if func in poss_set:
                    poss_set.remove(func)
    pprint(codes_to_funcs)

    # Execute program
    registers = [0] * 4
    for opcode, a, b, c in program:
        registers = codes_to_funcs[opcode](registers, a, b, c)
    return registers

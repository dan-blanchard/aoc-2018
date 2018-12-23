from collections import Counter, defaultdict
from pprint import pprint


def addr(registers, a, b, c):
    """(add register) stores into register C the result of adding register A and register B."""
    registers[c] = registers[a] + registers[b]


def addi(registers, a, b, c):
    """(add immediate) stores into register C the result of adding register A and value B."""
    registers[c] = registers[a] + b


def mulr(registers, a, b, c):
    """(multiply register) stores into register C the result of multiplying register A and register B."""
    registers[c] = registers[a] * registers[b]


def muli(registers, a, b, c):
    """(multiply immediate) stores into register C the result of multiplying register A and value B."""
    registers[c] = registers[a] * b


def banr(registers, a, b, c):
    """(bitwise AND register) stores into register C the result of the bitwise AND of register A and register B."""
    registers[c] = registers[a] & registers[b]


def bani(registers, a, b, c):
    """(bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B."""
    registers[c] = registers[a] & b


def borr(registers, a, b, c):
    """(bitwise OR register) stores into register C the result of the bitwise OR of register A and register B."""
    registers[c] = registers[a] | registers[b]


def bori(registers, a, b, c):
    """(bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B."""
    registers[c] = registers[a] | b


def setr(registers, a, b, c):
    """(set register) copies the contents of register A into register C. (Input B is ignored.)"""
    registers[c] = registers[a]


def seti(registers, a, b, c):
    """(set immediate) stores value A into register C. (Input B is ignored.)"""
    registers[c] = a


def gtir(registers, a, b, c):
    """(greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0."""
    registers[c] = int(a > registers[b])


def gtri(registers, a, b, c):
    """(greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0."""
    registers[c] = int(registers[a] > b)


def gtrr(registers, a, b, c):
    """(greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0."""
    registers[c] = int(registers[a] > registers[b])


def eqir(registers, a, b, c):
    """(equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0."""
    registers[c] = int(a == registers[b])


def eqri(registers, a, b, c):
    """(equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0."""
    registers[c] = int(registers[a] == b)


def eqrr(registers, a, b, c):
    """(equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0."""
    registers[c] = int(registers[a] == registers[b])


def parse_puzzle(puzzle_input_file):
    program = []
    ip = None
    with open(puzzle_input_file, "r") as puzzle_input:
        for line in puzzle_input:
            line = line.strip()
            if line.startswith("#ip"):
                ip = int(line.split()[1])
            else:
                op, a, b, c = line.split()
                program.append((eval(op), int(a), int(b), int(c)))
    return ip, program


def run_puzzle_program(puzzle_input_file, registers, verbose=False):
    ip, program = parse_puzzle(puzzle_input_file)
    num_instr = len(program)
    halt_set = set()
    last_halter = None
    while registers[ip] < num_instr:
        instr, a, b, c = program[registers[ip]]
        if verbose:
            print(f"ip={ip} {registers} {instr.__name__} {a} {b} {c}", end=" ")
        # Save values that would cause program to halt
        if registers[ip] == 28:
            if registers[3] not in halt_set:
                halt_set.add(registers[3])
                last_halter = registers[3]
            else:
                print("Saw repeat, stopping")
                print(
                    f"Highest: {max(halt_set)}\t Lowest: {min(halt_set)}\t Last: {last_halter}"
                )
                break
        instr(registers, a, b, c)
        if verbose:
            print(registers)
        registers[ip] += 1
    return registers

import re

INPUT = "input.txt"


def read_input() -> tuple[list[int], list[int]]:
    with open(INPUT) as f:
        r, p = f.read().split("\n\n")
        registers = list(map(int, re.findall(r"\d+", r)))
        program = list(map(int, re.findall(r"\d+", p)))
        return registers, program


class Program:
    def __init__(self, registers: list[int]):
        self.A, self.B, self.C = registers

    def execute(self, program: list[int]) -> list[int]:
        """
        Execute the program and return the result
        :param program: Program to run. A set of pairs of optcode and operand
        :return: Output of the program (optcode 5)
        """
        ip = 0  # instruction pointer
        result = []

        while ip < len(program):

            combo_values = {0: 0, 1: 1, 2: 2, 3: 3, 4: self.A, 5: self.B, 6: self.C}
            optcode = program[ip]
            operand = program[ip + 1]

            match optcode:
                case 0:  # `adv`: division A // (2 ^ combo operand) - store in `A`
                    denominator = 2 ** combo_values[operand]
                    self.A = self.A // denominator
                case 1:  # `bxl`: bitwise XOR B ^ operand - store in `B`
                    self.B = self.B ^ operand
                case 2:  # `bst`: combo operand modulo 8 - store in `B`
                    self.B = combo_values[operand] % 8
                case 3:  # `jnz`: jump by operand if `A` is not zero
                    if self.A != 0:
                        ip = operand
                        continue
                case 4:  # `bxc`: bitwise XOR B ^ C - store in `C`
                    self.B = self.B ^ self.C
                case 5:  # `out`: combo operand modulo 8 - append to `result`
                    result.append(combo_values[operand] % 8)
                case 6:  # `bdv`: division A // (2 ^ combo operand) - store in `B`
                    denominator = 2 ** combo_values[operand]
                    self.B = self.A // denominator
                case 7:  # `cdv`: division A // (2 ^ combo operand) - store in `C`
                    denominator = 2 ** combo_values[operand]
                    self.C = self.A // denominator

            # increment instruction pointer by 2
            ip += 2

        return result

    def find_a_register_value(self, program: list[int]) -> int:
        """
        Get a value of `A` register to find output being a copy of itself
        :param program: Program to run. A set of pairs of optcode and operand
        :return: Value of `A` that will halt the program
        """
        results: list[int] = []
        # Start from end of the program
        todos: list[tuple[int, int]] = [(len(program) - 1, 0)]
        for position, value in todos:
            # Try all values from 0 to 7
            for a in range(value * 8, (value + 1) * 8):
                # Create a new program with the new value of `A`
                p = Program([a, self.B, self.C])
                # Execute the program from the given position
                if p.execute(program) == program[position:]:
                    # If the output is the same as the remaining program
                    if position == 0:
                        # If we are at the beginning of the program, add the value to the results
                        results.append(a)
                    else:
                        # Otherwise, add the new position and value to the todos
                        todos.append((position - 1, a))

        return min(results)


def main():
    registers, program = read_input()
    p = Program(registers)
    result = p.execute(program)
    print(f"The result of program: {','.join(map(str, result))}")

    a = p.find_a_register_value(program)
    print(f"The value of `A` for program copy: {a}")


if __name__ == "__main__":
    main()

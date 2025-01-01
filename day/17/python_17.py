import re

INPUT = "input.txt"
# INPUT = "input_example.txt"


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


def main():
    registers, program = read_input()
    p = Program(registers)
    result = p.execute(program)
    print(f"The result is {','.join(map(str, result))}")


if __name__ == "__main__":
    main()

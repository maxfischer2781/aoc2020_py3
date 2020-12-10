from typing import NamedTuple, Literal, get_args, List, Tuple, Iterable

FORMAT = """
Default Accumulated: {}
Fixed Accumulated: {}
"""


def solve(in_stream):
    instructions = [Instruction.from_str(line) for line in in_stream]
    default = run_once(instructions)[0]
    for new_instructions in swap_instructions(instructions):
        total, proper = run_once(new_instructions)
        if proper:
            return default, total


class Instruction(NamedTuple):
    operation: Literal['jmp', 'acc', 'nop']
    argument: int

    @classmethod
    def from_str(cls, literal: str):
        """Read a literal such as  `jmp +4`"""
        op, arg = literal.split()
        assert op in get_args(cls.__annotations__['operation'])
        return cls(op, int(arg))

    def apply(self, pointer, total):
        if self.operation == 'jmp':
            return pointer + self.argument, total
        elif self.operation == 'acc':
            return pointer + 1, total + self.argument
        elif self.operation == 'nop':
            return pointer + 1, total
        else:
            raise ValueError(f'Unknown operation {self.operation}')


def run_once(instructions: List[Instruction]) -> Tuple[int, bool]:
    """
    Run `instructions` until hitting a loop or terminating

    :return: accumulated value and whether termination was proper.
    """
    seen = set()
    total = 0
    pointer = 0
    while pointer not in seen and pointer < len(instructions):
        seen.add(pointer)
        pointer, total = instructions[pointer].apply(pointer, total)
    return total, pointer >= len(instructions)


def swap_instructions(instructions: List[Instruction]) -> Iterable[List[Instruction]]:
    """Generate new `instructions` by swapping each JMP/NOP instruction once"""
    for index in reversed(range(len(instructions))):
        instruction = instructions[index]
        if instruction.operation != 'acc':
            yield [
                *instructions[:index],
                Instruction(
                    'jmp' if instruction.operation == 'nop' else 'nop',
                    instruction.argument,
                ),
                *instructions[index+1:]
            ]

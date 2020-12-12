from typing import Iterable, List, Tuple


FORMAT = """
followed: {}
navigated: {}
"""


def solve(instream):
    instructions = read(instream)
    return manhattan(follow(instructions)), manhattan(navigate(instructions))


def read(source: Iterable[str]) -> List[Tuple[str, int]]:
    return [(arg[0], int(arg[1:])) for arg in source]


# use complex numbers of x+yj as 2D coordinates
NORTH = 1j
SOUTH = -1j
EAST = 1+0j
WEST = -1+0j
# rotations
ROT = {0: 1, 90: 1j, 180: -1, 270: -1j}


def manhattan(position: complex) -> int:
    return int(abs(position.real) + abs(position.imag))


def follow(instructions: List[Tuple[str, int]]) -> complex:
    position, orientation = 0j, EAST
    for op, arg in instructions:
        if op == 'N':
            position += NORTH * arg
        elif op == 'S':
            position += SOUTH * arg
        elif op == 'E':
            position += EAST * arg
        elif op == 'W':
            position += WEST * arg
        elif op == 'F':
            position += orientation * arg
        elif op == 'L':
            orientation *= ROT[arg % 360]
        elif op == 'R':
            orientation *= ROT[-arg % 360]
        else:
            raise ValueError(f"Unknown operation: {op!r}")
    return position


def navigate(instructions: List[Tuple[str, int]]) -> complex:
    position, waypoint = 0j, NORTH + 10 * EAST
    for op, arg in instructions:
        if op == 'N':
            waypoint += NORTH * arg
        elif op == 'S':
            waypoint += SOUTH * arg
        elif op == 'E':
            waypoint += EAST * arg
        elif op == 'W':
            waypoint += WEST * arg
        elif op == 'F':
            position += waypoint * arg
        elif op == 'L':
            waypoint *= ROT[arg % 360]
        elif op == 'R':
            waypoint *= ROT[-arg % 360]
        else:
            raise ValueError(f"Unknown operation: {op!r}")
    return position

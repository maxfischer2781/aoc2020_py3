from typing import NamedTuple, Iterable, Tuple, TypeVar

FORMAT = """
Max seat ID: {0}
Mid seat ID: {1}
"""


def solve(in_stream):
    seats = [Seat.from_str(line.strip()) for line in in_stream]
    seats.sort(key=lambda seat: seat.id)
    for prev, next in pairwise(seats):
        if next.id - prev.id == 2:
            return seats[-1].id, prev.id + 1


T = TypeVar('T')


def pairwise(iterable: Iterable[T]) -> Iterable[Tuple[T, T]]:
    """Iterate overlapping pairs as (a0, a1, a2, ...) -> ((a0, a1), (a1, a2), ...)"""
    iterator = iter(iterable)
    a = next(iterator)
    for b in iterator:
        yield a, b
        a = b


class Seat(NamedTuple):
    row: int
    column: int

    @property
    def id(self) -> int:
        return self.row * 8 + self.column

    @classmethod
    def from_str(cls, literal: str):
        """Read a literal such as `BFFFBBFRRR` to `70, 7`"""
        return cls(
            sum(
                (2 ** (6 - index)) if fb == "B" else 0
                for index, fb in enumerate(literal[:7])
            ),
            sum(
                (2 ** (2 - index)) if lr == "R" else 0
                for index, lr in enumerate(literal[7:])
            ),
        )
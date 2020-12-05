import pathlib
from functools import reduce


def solve():
    data_path = pathlib.Path(__file__).parent.parent / "data/day3.txt"
    with data_path.open() as in_stream:
        data = [MapLine.from_str(line) for line in in_stream]
    print("Hits simple", sum_slope(data, 3, 1))
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    slope_hits = [sum_slope(data, *slope) for slope in slopes]
    print("Hits many", reduce(lambda a, b: a * b, slope_hits))


def sum_slope(map_lines, right: int, down: int) -> int:
    hits = 0
    for index, line in enumerate(map_lines):
        if index % down == 0:
            hits += line[index // down * right]
    return hits


class MapLine:
    def __init__(self, *fields):
        self._fields = fields

    @classmethod
    def from_str(cls, literal: str):
        return cls(*(field == "#" for field in literal.strip()))

    def __str__(self):
        return f"[{''.join('#' if field else '.' for field in self._fields)}]"

    def __getitem__(self, item):
        return self._fields[item % len(self._fields)]

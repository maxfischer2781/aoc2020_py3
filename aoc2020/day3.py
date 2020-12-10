from math import prod

FORMAT = """
Hits 3:1 {}
Hits all {}
"""


def solve(in_stream):
    data = [MapLine.from_str(line) for line in in_stream]
    simple_hits = sum_slope(data, 3, 1)
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    slope_hits = [sum_slope(data, *slope) for slope in slopes]
    return simple_hits, prod(slope_hits)


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

from typing import Iterable, TypeVar, Tuple
from itertools import islice
from collections import deque

T = TypeVar('T')
FORMAT = """
Window sum outlier: {0}
Window sum min/max: {1}
"""


def solve(in_stream):
    series = [int(line) for line in in_stream]
    outlier = find_nonsum(series, 25)
    print("Window sum outlier:", outlier)
    sum_min, sum_max = find_sum(series, total=outlier)
    return outlier, sum_min + sum_max


def windowed(items: Iterable[T], size: int) -> Iterable[Tuple[T, ...]]:
    """Iterate over all windows of ``size`` in `items``"""
    items = iter(items)
    window = deque(islice(items, size - 1), maxlen=size)
    for item in items:
        window.append(item)
        yield tuple(window)


def find_nonsum(series: Iterable[int], window_size: int) -> int:
    """Find the number which is not the sum of its preceding window"""
    for *window, item in windowed(series, window_size + 1):
        window = set(window)
        if not any((item - other) in window for other in window):
            return item
    raise ValueError("series contains no item with sum of previous window")


def find_sum(series: Iterable[int], total) -> Tuple[int, int]:
    """Find min/max of the window which sums to `total`"""
    window = deque()
    sum = 0
    # This algorithm relies on all items being positive
    # This means when `sum` is too high/low we must *always* remove/add items
    for item in series:
        while sum > total:
            sum -= window.popleft()
        if sum == total and len(window) >= 2:
            window = sorted(window)
            return window[0], window[-1]
        else:
            window.append(item)
            sum += item
    raise ValueError("series contains no window with sum of total")

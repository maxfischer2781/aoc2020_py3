from typing import List
from math import prod


FORMAT = """
Jolt step product: {0}
Adapter variations: {1}
"""


def solve(in_stream):
    connectors = [int(line) for line in in_stream]
    steps = shortest_steps(connectors)
    step_counts = count(steps)
    return step_counts[0] * step_counts[1], variations(steps)


def shortest_steps(connectors: List[int]):
    """
    Compute the sequence of steps (differences) by connecting all adapters
    """
    connectors = sorted(connectors)
    return [nxt-prv for prv, nxt in zip([0]+connectors, connectors)] + [3]


def count(steps: List[int]):
    """Get the count of 1-step and 3-step jolt connections"""
    # this needs two passes but does them with a builtin
    # the factor 2x should be much smaller than the Python vs Builtin factor
    return steps.count(1), steps.count(3)


def variations(steps: List[int]):
    """
    Compute the variations to connect the outlet to the device given adapter steps

    .. note::

        This algorithm relies on steps being either 1 or 3.
    """
    # we can only vary parts *between* 3-step connectors
    fixed_indices = [i for i, step in enumerate(steps) if step == 3]
    lengths = [
        next_i - prev_i - 1 for prev_i, next_i in zip(
            [-1] + fixed_indices, fixed_indices
        )
    ]
    # cache for variations of each sequence length we need
    cache = [1, 1, 2, 4]
    for i in range(len(cache), max(lengths) + 1):
        # f(n) = f(n-1) + f(n-2) + f(n-3)
        #      = f(n-1) + f(n-2) + f(n-3) + f(n-4) - f(n-4)
        #      = 2 f(n-1) - f(n-4)
        cache.append(2 * cache[i-1] - cache[i-4])
    return prod(map(cache.__getitem__, lengths))

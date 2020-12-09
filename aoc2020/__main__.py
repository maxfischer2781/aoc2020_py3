import argparse
import time

from . import day1
from . import day2
from . import day3
from . import day4
from . import day5
from . import day6
from . import day7
from . import day8
from . import day9

SOLUTIONS = {
    index: module.solve
    for index, module in enumerate(
        (day1, day2, day3, day4, day5, day6, day7, day8, day9),
        start=1,
    )
}


def format_duration(delta: float):
    symbol = 's'
    for i, symbol in enumerate(("us", "ms", "ns"), start=1):
        if delta > (10**(-3*i + 1)):
            break
        delta = delta * 1000
    return f"{delta:.2f} {symbol}"


CLI = argparse.ArgumentParser()
CLI.add_argument(
    'DAY',
    default=max(SOLUTIONS),
    nargs='?',
    type=int,
    choices=list(SOLUTIONS)
)

opts = CLI.parse_args()
solver = SOLUTIONS[opts.DAY]
pre = time.time()
solver()
end = time.time()

print(f"[Elapsed {format_duration(end-pre)}]")

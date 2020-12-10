import argparse
import time
import pathlib
import io

from . import day1
from . import day2
from . import day3
from . import day4
from . import day5
from . import day6
from . import day7
from . import day8
from . import day9
from . import day10

SOLUTIONS = dict(
    enumerate(
        (day1, day2, day3, day4, day5, day6, day7, day8, day9, day10),
        start=1,
    )
)


def format_duration(delta: float):
    for symbol in ("s", "ms", "μs", "ns"):
        if delta > 0.5:
            break
        delta = delta * 1000
    return f"{delta:.2f} {symbol}"


def run_solution(day: int):
    print(f"[> ### Day {day:3d} ### <]")
    input_path = pathlib.Path(__file__).parent.parent / 'data' / f'day{day}.txt'
    data = io.StringIO(input_path.read_text())
    solver, template = SOLUTIONS[day].solve, SOLUTIONS[day].FORMAT.strip()
    pre = time.time()
    results = solver(data)
    end = time.time()
    print(template.format(*results))
    print(f"[> Elapsed {format_duration(end-pre)} <]")


CLI = argparse.ArgumentParser()
CLI.add_argument(
    'DAY',
    default=[],
    nargs='*',
    type=int,
)

opts = CLI.parse_args()
for d in opts.DAY or [max(SOLUTIONS)]:
    assert d in SOLUTIONS, f"days {', '.join(map(str, SOLUTIONS))} available, not {d}"
    run_solution(d)

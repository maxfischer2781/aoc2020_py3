import argparse
from . import day1
from . import day2
from . import day3
from . import day4
from . import day5
from . import day6
from . import day7
from . import day8

SOLUTIONS = {
    index: module.solve
    for index, module in enumerate(
        (day1, day2, day3, day4, day5, day6, day7, day8),
        start=1,
    )
}

CLI = argparse.ArgumentParser()
CLI.add_argument(
    'DAY',
    default=8,
    nargs='?',
    type=int,
    choices=list(SOLUTIONS)
)

opts = CLI.parse_args()
SOLUTIONS[opts.DAY]()

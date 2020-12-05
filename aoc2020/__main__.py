import argparse
from . import day1
from . import day2

SOLUTIONS = {
    1: day1.solve,
    2: day2.solve,
}

CLI = argparse.ArgumentParser()
CLI.add_argument(
    'DAY',
    default=2,
    nargs='?',
    type=int,
    choices=list(SOLUTIONS)
)

opts = CLI.parse_args()
SOLUTIONS[opts.DAY]()

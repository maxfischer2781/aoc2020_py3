import argparse
from . import day1

SOLUTIONS = {
    1: day1.solve
}

CLI = argparse.ArgumentParser()
CLI.add_argument(
    'DAY',
    default=1,
    nargs='?',
    type=int,
    choices=list(SOLUTIONS)
)

opts = CLI.parse_args()
SOLUTIONS[opts.DAY]()

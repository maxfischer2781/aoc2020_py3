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
    1: day1.solve,
    2: day2.solve,
    3: day3.solve,
    4: day4.solve,
    5: day5.solve,
    6: day6.solve,
    7: day7.solve,
    8: day8.solve,
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

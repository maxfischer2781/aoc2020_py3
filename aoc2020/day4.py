from typing import Iterable, Dict


def solve(in_stream):
    data = list(read_passports(in_stream))
    complete_passports = [passport for passport in data if is_complete(passport)]
    print(f"No compl {len(complete_passports)}")
    valid_passports = [passport for passport in complete_passports if is_valid(passport)]
    print(f"No valid {len(valid_passports)}")


def is_complete(passport: Dict[str, str]):
    missing_keys = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"} - passport.keys()
    return not missing_keys


def is_literal_range(literal: str, min: int, max: int) -> bool:
    try:
        value = int(literal)
    except ValueError:
        return False
    else:
        return min <= value <= max


PASSPORT_PREDICATES = {
    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    "byr": lambda value: is_literal_range(value, 1920, 2002),
    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    "iyr": lambda value: is_literal_range(value, 2010, 2020),
    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    "eyr": lambda value: is_literal_range(value, 2020, 2030),
    # hgt (Height) - a number followed by either cm or in:
    "hgt": lambda value: (
        lambda digits, unit:
            # If cm, the number must be at least 150 and at most 193.
            is_literal_range(digits, 150, 193) if unit == "cm" else
            # If in, the number must be at least 59 and at most 76.
            is_literal_range(digits, 59, 76) if unit == "in" else
            False
        )(value[:-2], value[-2:]),
    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    "hcl": lambda value: (
            len(value) == 7
            and value.startswith("#")
            and set(value[1:]) <= {*"0123456789abcdef"}
    ),
    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    "ecl": lambda value: value in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"},
    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    "pid": lambda value: len(value) == 9 and is_literal_range(value, 0, 999999999),
}


def is_valid(passport: Dict[str, str]):
    assert is_complete(passport), "only check complete passports for validity"
    return all(
        predicate(passport[key])
        for key, predicate in PASSPORT_PREDICATES.items()
    )


def read_passports(in_stream: Iterable[str]) -> Iterable[Dict[str, str]]:
    """Read consecutive Passport batches from a stream"""
    current = {}
    for line in map(str.strip, in_stream):
        # passports are separate by empty lines
        if not line and current:
            yield current
            current = {}
        else:
            # parse a line such as `iyr:2017 hgt:160cm`
            current.update(
                {key: value for key, value in (kv.split(':') for kv in line.split())}
            )
    if current:
        yield current

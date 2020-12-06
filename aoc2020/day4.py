from typing import Iterable, Dict
import pathlib


def solve():
    data_path = pathlib.Path(__file__).parent.parent / "data/day4.txt"
    with data_path.open() as in_stream:
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


def is_valid(passport: Dict[str, str]):
    assert is_complete(passport), "only check complete passports for validity"
    # TODO: Having a dict of {key: predicate} would be more idiomatic
    return (
        # byr (Birth Year) - four digits; at least 1920 and at most 2002.
        is_literal_range(passport["byr"], 1920, 2002) and
        # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        is_literal_range(passport["iyr"], 2010, 2020) and
        # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        is_literal_range(passport["eyr"], 2020, 2030) and
        # hgt (Height) - a number followed by either cm or in:
        (
            lambda digits, unit:
                # If cm, the number must be at least 150 and at most 193.
                is_literal_range(digits, 150, 193) if unit == "cm" else
                # If in, the number must be at least 59 and at most 76.
                is_literal_range(digits, 59, 76) if unit == "in" else
                False
        )(passport["hgt"][:-2], passport["hgt"][-2:]) and
        # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        len(passport["hcl"]) == 7 and
        passport["hcl"].startswith("#") and
        set(passport["hcl"][1:]) <= {*"0123456789abcdef"} and
        # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        passport["ecl"] in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"} and
        # pid (Passport ID) - a nine-digit number, including leading zeroes.
        len(passport["pid"]) == 9 and
        is_literal_range(passport["pid"], 0, 999999999)
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

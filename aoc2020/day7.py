from typing import Dict, Tuple, List
import re


def solve(in_stream):
    color_contains = {
        color: contains for color, contains in map(parse_bag_spec, in_stream)
    }
    color_containing = inverse_contains(color_contains)
    print("Unique parents", unique_containing(color_containing, "shiny gold"))
    print("Total children", total_contained(color_contains, "shiny gold") - 1)


CONTAINED_PATTERN = re.compile(r"(\d+)\s+(\w+\s+\w+)\s+bag")


def parse_bag_spec(line: str) -> Tuple[str, Dict[str, int]]:
    color, _, contained = line.partition(" bags contain ")
    return color.strip(), {
        match.group(2): int(match.group(1))
        for match in CONTAINED_PATTERN.finditer(contained)
    }


def inverse_contains(contains: Dict[str, Dict[str, int]]) -> Dict[str, List[str]]:
    containing = {}
    for color, children in contains.items():
        for contained in children:
            containing.setdefault(contained, []).append(color)
    return containing


def unique_containing(containing: Dict[str, List[str]], root: str):
    """Count the number of unique colors eventually containing `root`"""
    seen = set()
    outstanding = {root}
    # destructively iterate to allow both growing and trimming
    while outstanding:
        node = outstanding.pop()
        seen.add(node)
        for parent in containing.get(node, []):
            if parent not in seen:
                outstanding.add(parent)
    return len(seen) - 1


def total_contained(contains: Dict[str, Dict[str, int]], root: str) -> int:
    """Count the total number of colors contained in `root`, including itself"""
    return 1 + sum(
        count * total_contained(contains, child) for child, count in contains[root].items()
    )

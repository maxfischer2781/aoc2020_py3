from typing import Iterable


FORMAT = """
Group sum any: {0}
Group sum all: {1}
"""


def solve(in_stream):
    # frozenset instead of set to avoid mutation by collecting sets
    questionnaires = [frozenset(line.strip()) for line in in_stream]
    groups_any = list(merge_groups(questionnaires, overlap=False))
    groups_all = list(merge_groups(questionnaires, overlap=True))
    return sum(map(len, groups_any)), sum(map(len, groups_all))


def merge_groups(questionnaires: Iterable[set], overlap: bool) -> Iterable[set]:
    current = None
    for questionnaire in questionnaires:
        if not questionnaire and current is not None:
            if current:
                yield current
            current = None
        elif current is None:
            current = questionnaire
        elif overlap:
            current &= questionnaire
        else:
            current |= questionnaire
    if current:
        yield current

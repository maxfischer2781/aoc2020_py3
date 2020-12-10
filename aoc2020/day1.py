FORMAT = """
Double product: {}
Triple product: {}
"""


def solve(in_stream):
    data = read(in_stream)
    da, db = search_double(data, total=2020)
    ta, tb, tc = search_triple(data, total=2020)
    return da * db, ta * tb * tc


def search_double(candidates: list, total: int):
    candidates = set(candidates)
    for num in candidates:
        if total - num in candidates:
            return num, total - num
    raise ValueError(f"No pair of candidates sums to {total}")


def search_triple(candidates: list, total: int):
    candidates = set(candidates)
    for num1 in candidates:
        for num2 in candidates:
            if total - num1 - num2 in candidates:
                return num1, num2, total - num1 - num2
    raise ValueError(f"No triple of candidates sums to {total}")


def read(in_stream):
    return [int(line) for line in in_stream]

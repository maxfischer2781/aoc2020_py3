from typing import NamedTuple

FORMAT = """
Range count {0}
Index count {1}
"""


def solve(in_stream):
    data = [PolicyPassword.from_str(line) for line in in_stream]
    return sum(pw.in_range() for pw in data), sum(pw.in_position() for pw in data)


class PolicyPassword(NamedTuple):
    min: int
    max: int
    symbol: str
    password: str

    @classmethod
    def from_str(cls, literal: str):
        """Parse a literal such as `3-7 x: xjxbgpxxgtx`"""
        head, symbol, password = literal.split()
        min, max = map(int, head.split('-'))
        return cls(min, max, symbol[:-1], password)

    def in_range(self):
        """Whether `symbol` appears between `min` and `max` times"""
        return self.min <= self.password.count(self.symbol) <= self.max

    def in_position(self):
        """Whether `symbol` appears either at the `min`'th or `max`'th position"""
        return (self.password[self.min - 1] == self.symbol) ^ (self.password[self.max - 1] == self.symbol)

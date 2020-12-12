from typing import NamedTuple, Dict, Tuple, Set, Iterable, List

FORMAT = "{} {}"


def solve(in_stream):
    data = list(in_stream)
    neighbouring = neighbouring_seats(data)
    print(neighbouring.evolve_stable().occupied)
    visible = visible_seats(data)
    print(visible.evolve_stable().occupied)
    return 1, 1


class Seats(NamedTuple):
    threshold: int
    positions: Dict[Tuple[int, int], List[Tuple[int, int]]]
    occupancy: Set[Tuple[int, int]]

    @property
    def occupied(self) -> int:
        return len(self.occupancy)

    def evolve_stable(self):
        prev_occupancy = None
        next_layout = self
        while next_layout.occupancy != prev_occupancy:
            prev_occupancy = next_layout.occupancy
            next_layout = next_layout.evolve_once()
        return next_layout

    def evolve_once(self) -> 'Seats':
        # we need these a lot
        threshold = self.threshold
        occupancy = self.occupancy
        new_occupancy = set()
        for position, neighbours in self.positions.items():
            count = sum(1 for npos in neighbours if npos in occupancy)
            if count == 0 or (count < threshold and position in occupancy):
                new_occupancy.add(position)
        return Seats(self.threshold, self.positions, new_occupancy)


def _read_seats(layout: Iterable[str]) -> Set[Tuple[int, int]]:
    return {
        (ri, ci)
        for ri, row in enumerate(layout)
        for ci, seat in enumerate(row) if seat == 'L'
    }


def neighbouring_seats(layout: Iterable[str]) -> Seats:
    seats = _read_seats(layout)
    positions = {
        (ri, ci): [
            (ri + ro, ci + co) for ro, co in [
                [1, 1], [1, 0], [1, -1], [0, 1], [0, -1], [-1, 1], [-1, 0], [-1, -1]
            ]
        ]
        for ri, ci in seats
    }
    return Seats(4, positions, set())


def visible_seats(layout: Iterable[str]) -> Seats:
    seats = _read_seats(layout)
    positions = {pos: [] for pos in seats}
    max_ri, max_ci = max(ri for ri, _ in seats), max(ci for _, ci in seats)
    # horizontal
    for ri in range(max_ri + 1):
        prev = None
        for ci in range(max_ci + 1):
            pos = (ri, ci)
            if pos in seats:
                if prev is not None:
                    positions[pos].append(prev)
                    positions[prev].append(pos)
                prev = pos
    # vertical
    for ci in range(max_ci + 1):
        prev = None
        for ri in range(max_ri + 1):
            if pos in seats:
                if prev is not None:
                    positions[pos].append(prev)
                    positions[prev].append(pos)
                prev = pos
    # diagonal -> right, down
    # 0,0 0,1 c-r=2
    # 1,0 1,1 c-r=1
    #         c-r=0
    for total in range(-max_ri, max_ci + 1):
        prev = None
        for ri in range(max_ri + 1):
            pos = (ri, total + ri)
            if pos in seats:
                if prev is not None:
                    positions[pos].append(prev)
                    positions[prev].append(pos)
                prev = pos
    # diagonal -> left, down
    #       0,0 0,1
    # c+r=0 1,0 1,1
    # c+r=1 c+r=2
    for total in range(max_ri + max_ci + 1):
        prev = None
        for ri in range(max_ri + 1):
            pos = (ri, total - ri)
            if pos in seats:
                if prev is not None:
                    positions[pos].append(prev)
                    positions[prev].append(pos)
                prev = pos
    return Seats(5, positions, set())

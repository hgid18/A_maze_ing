import random
from typing import Optional
from .cell import Cell, directions, opposite_directions


class MazeGenerator:

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    seed: Optional[int]
    perfect: bool
    grid: list[list[Cell]]
    blocked: set[tuple[int, int]]

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        seed: Optional[int] = None,
        perfect: bool = False,
    ) -> None:

        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.seed = seed
        self.perfect = perfect
        self.blocked: set[tuple[int, int]] = set()

        self.grid = []

        for row in range(self.height):
            current_row = []
            for col in range(self.width):
                current_row.append(Cell(row=row, col=col))
            self.grid.append(current_row)

    def create_42(self) -> None:
        pattern = [
            "1010111",
            "1010001",
            "1110111",
            "0010100",
            "0010111"
        ]
        pattern_height = len(pattern)
        pattern_width = len(pattern[0])

        if self.height < pattern_height or self.width < pattern_width:
            print("Entry overlaps the 42 pattern.")
            return

        start_row = self.height // 2 - pattern_height // 2
        start_col = self.width // 2 - pattern_width // 2

        for r in range(pattern_height):
            for c in range(pattern_width):
                if pattern[r][c] == "1":
                    self.blocked.add((start_row + r, start_col + c))

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.height and 0 <= col < self.width

    def cell_at(self, row: int, col: int) -> Cell:
        return self.grid[row][col]

    def neighbors(self, row: int, col: int) -> list[tuple[int, int, int]]:
        result = []

        for direction, (drow, dcol) in directions.items():
            nrow = row + drow
            ncol = col + dcol

            if self.in_bounds(nrow, ncol):
                result.append((direction, nrow, ncol))

        return result

    def carve_passage(
        self,
        row: int,
        col: int,
        direction: int,
        nrow: int,
        ncol: int,
    ) -> None:
        current = self.cell_at(row, col)
        neighbor = self.cell_at(nrow, ncol)

        current.remove_wall(direction)
        neighbor.remove_wall(opposite_directions[direction])

    def add_random_passages(self) -> None:
        available_passages = []

        for row in range(self.height):
            for col in range(self.width):
                if (row, col) in self.blocked:
                    continue

                cell = self.cell_at(row, col)
                for direction, (drow, dcol) in directions.items():
                    nrow, ncol = row + drow, col + dcol

                    if not self.in_bounds(nrow, ncol):
                        continue
                    if (nrow, ncol) in self.blocked:
                        continue

                    if cell.has_wall(direction):
                        available_passages.append(
                            (direction, row, col, nrow, ncol)
                        )

        num_to_open = max(1, len(available_passages) // 5)
        passages_to_open = random.sample(available_passages,
                                         min(num_to_open,
                                             len(available_passages)))

        for direction, row, col, nrow, ncol in passages_to_open:
            self.carve_passage(row, col, direction, nrow, ncol)

    def generate(self) -> None:

        self.create_42()

        if self.seed is not None:
            random.seed(self.seed)

        visited = set()

        def dfs(row: int, col: int) -> None:
            visited.add((row, col))

            neigh = self.neighbors(row, col)
            random.shuffle(neigh)

            for direction, nrow, ncol in neigh:

                if (nrow, ncol) in self.blocked:
                    continue

                if (nrow, ncol) not in visited:
                    self.carve_passage(
                        row=row,
                        col=col,
                        direction=direction,
                        nrow=nrow,
                        ncol=ncol,
                    )
                    dfs(nrow, ncol)

        start_x, start_y = self.entry

        dfs(start_y, start_x)

        if not self.perfect:
            self.add_random_passages()
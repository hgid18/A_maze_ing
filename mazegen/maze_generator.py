import random
from .cell import Cell, directions, opposite_directions
from config_parser import ConfigMaze


class MazeGenerator:
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    grid: list[list[Cell]]

    def __init__(self, config: ConfigMaze) -> None:
        self.width = config.WIDTH
        self.height = config.HEIGHT
        self.entry = config.ENTRY
        self.exit = config.EXIT
        self.seed = config.SEED

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

        # Si el grid es demasiado pequeño, no dibujar el patrón
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

    def generate(self) -> None:
        """Genera un laberinto perfecto usando DFS recursivo."""

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

        # ENTRY está en formato (x, y)
        start_x, start_y = self.entry

        dfs(start_y, start_x)

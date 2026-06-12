import random
from cell import Cell
from cell import directions, opposite_directions
from config_parser import ConfigMaze


class Maze:
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

        self.grid = []

        for row in range(self.height):
            current_row = []
            for col in range(self.width):
                current_row.append(Cell(row=row, col=col))
            self.grid.append(current_row)

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

        if self.seed is not None:
            random.seed(self.seed)

        visited = set()

        def dfs(row: int, col: int) -> None:
            visited.add((row, col))

            neigh = self.neighbors(row, col)
            random.shuffle(neigh)

            for direction, nrow, ncol in neigh:
                if (nrow, ncol) not in visited:
                    self.carve_passage(
                        row,
                        col,
                        direction,
                        nrow,
                        ncol,
                    )
                    dfs(nrow, ncol)

        # ENTRY está en formato (x, y)
        start_x, start_y = self.entry
        dfs(start_y, start_x)

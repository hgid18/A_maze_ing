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
        self.grid = []

        for row in range(self.height):
            current_row: list[Cell] = []
            for col in range(self.width):
                cell = Cell(row=row, col=col)

                if (col, row) == self.entry:
                    cell.is_entry = True
                if (col, row) == self.exit:
                    cell.is_exit = True

                current_row.append(cell)
            self.grid.append(current_row)

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.height and 0 <= col < self.width

    def cell_at(self, row: int, col: int) -> Cell:
        return self.grid[row][col]

    def neighbors(self, row: int, col: int) -> list[tuple[int, int, int]]:
        result: list[tuple[int, int, int]] = []

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

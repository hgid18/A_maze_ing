from cell import Cell, north, south, east, west, walls
from cell import directions, opposite_directions
from config_parser import config_file, ConfigMaze
import random


class Maze:
    widht: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    grid: list[list[Cell]]

    def __init__(self, config: ConfigMaze) -> None:
        self.width = config.WIDTH
        self.height = config.HEIGHT
        self.entry = config.ENTRY
        self.exit = config.EXIT
        self.grid = [[Cell(row=r, col=c) for c in range(self.width)]
                     for r in range(self.height)]

    def generate(self) -> None:

        if hasattr(self, "seed") and self.seed is not None:
            random.seed(self.seed)

        visited: set[tuple[int, int]] = set()

        def dfs(row: int, col: int) -> None:
            visited.add((row, col))

            neighbors = self.neighbors(row, col)
            random.shuffle(neighbors)

            for direction, nrow, ncol in neighbors:
                if (nrow, ncol) not in visited:
                    self.carve_passage(
                        row=row,
                        col=col,
                        direction=direction,
                        nrow=nrow,
                        ncol=ncol,
                    )

                    dfs(nrow, ncol)

        start_col, start_row = self.entry
        dfs(start_row, start_col)

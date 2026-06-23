"""Main entry point for the A-Maze-ing maze generator."""

import sys
from collections import deque
from typing import Deque, Dict, List, Optional, Tuple

from mazegen.cell import directions, directions_letters, east, south
from config_parser import config_file
from mazegen.maze_generator import MazeGenerator

Coord = Tuple[int, int]


def cell_to_hex(walls_state: int) -> str:
    return format(walls_state, 'X')


class MazeSolver:
    def __init__(self, maze: MazeGenerator) -> None:
        self.maze = maze

    def _open_neighbors(
        self, row: int, col: int
    ) -> List[Tuple[int, int, int]]:
        cell = self.maze.cell_at(row, col)
        result: List[Tuple[int, int, int]] = []
        for direction, (drow, dcol) in directions.items():
            if cell.has_wall(direction):
                continue
            nrow, ncol = row + drow, col + dcol
            if self.maze.in_bounds(nrow, ncol):
                result.append((direction, nrow, ncol))
        return result

    def shortest_path(self) -> Optional[List[str]]:
        start_x, start_y = self.maze.entry
        end_x, end_y = self.maze.exit
        start: Coord = (start_y, start_x)
        end: Coord = (end_y, end_x)

        if not self.maze.in_bounds(*start) or not self.maze.in_bounds(*end):
            return None
        if start == end:
            return []

        visited = {start}
        queue: Deque[Coord] = deque([start])
        came_from: Dict[Coord, Tuple[Coord, int]] = {}

        while queue:
            row, col = queue.popleft()
            if (row, col) == end:
                return self._rebuild_path(came_from, start, end)
            for direction, nrow, ncol in self._open_neighbors(row, col):
                neighbor = (nrow, ncol)
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                came_from[neighbor] = ((row, col), direction)
                queue.append(neighbor)
        return None

    @staticmethod
    def _rebuild_path(
        came_from: Dict[Coord, Tuple[Coord, int]],
        start: Coord,
        end: Coord,
    ) -> List[str]:
        path: List[str] = []
        current = end
        while current != start:
            previous, direction = came_from[current]
            path.append(directions_letters[direction])
            current = previous
        path.reverse()
        return path


ANSI_RESET = "\033[0m"
ANSI_GREEN = "\033[92m"
ANSI_RED = "\033[91m"
ANSI_CYAN = "\033[96m"
ANSI_YELLOW = "\033[93m"

WALL_COLORS = [
    ("white",   "\033[97m"),
    ("red",     "\033[91m"),
    ("green",   "\033[92m"),
    ("yellow",  "\033[93m"),
    ("blue",    "\033[94m"),
    ("magenta", "\033[95m"),
    ("cyan",    "\033[96m"),
]


def display_ascii(
    maze: MazeGenerator,
    path: Optional[List[str]] = None,
    show_path: bool = False,
    wall_color: str = "\033[97m",
) -> None:
    path_cells: set[Tuple[int, int]] = set()
    if show_path and path:
        start_x, start_y = maze.entry
        row, col = start_y, start_x
        path_cells.add((row, col))
        move = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
        for letter in path:
            dr, dc = move[letter]
            row += dr
            col += dc
            path_cells.add((row, col))

    ex, ey = maze.entry
    exx, exy = maze.exit

    print(wall_color + "+" + "---+" * maze.width + ANSI_RESET)

    for r in range(maze.height):
        line1 = wall_color + "|" + ANSI_RESET
        line2 = wall_color + "+" + ANSI_RESET

        for c in range(maze.width):
            cell = maze.cell_at(r, c)

            if (r, c) == (ey, ex):
                interior = ANSI_GREEN + " E " + ANSI_RESET
            elif (r, c) == (exy, exx):
                interior = ANSI_RED + " S " + ANSI_RESET
            elif show_path and (r, c) in path_cells:
                interior = ANSI_CYAN + " . " + ANSI_RESET
            elif cell.is_closed():
                interior = ANSI_YELLOW + "   " + ANSI_RESET
            else:
                interior = "   "

            line1 += interior
            line1 += (
                wall_color + "|" + ANSI_RESET
                if cell.has_wall(east) else " "
            )
            line2 += (
                wall_color + "---+" + ANSI_RESET
                if cell.has_wall(south)
                else "   " + wall_color + "+" + ANSI_RESET
            )

        print(line1)
        print(line2)


def export_hex(maze: MazeGenerator, path: List[str], filename: str) -> None:

    ex, ey = maze.entry
    exx, exy = maze.exit

    with open(filename, "w") as f:
        for r in range(maze.height):
            row_str = ""
            for c in range(maze.width):
                row_str += cell_to_hex(maze.grid[r][c].walls_state)
            f.write(row_str + "\n")

        f.write("\n")
        f.write(f"{ex},{ey}\n")
        f.write(f"{exx},{exy}\n")
        f.write("".join(path) + "\n")


def menu(maze: MazeGenerator, path: Optional[List[str]],
         filename: str) -> None:

    show_path = False
    wall_color_idx = 0
    wall_color = WALL_COLORS[wall_color_idx][1]
    display_ascii(maze, path, show_path, wall_color)

    while True:
        print("\n==== A-Maze-ing ====")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print(
            f"3. Change wall color "
            f"(current: {WALL_COLORS[wall_color_idx][0]})"
        )
        print("4. Quit")
        choice = input("Choice (1-4): ").strip()

        if choice == "1":
            from mazegen.cell import walls as _walls
            maze.blocked = set()
            for r in range(maze.height):
                for c in range(maze.width):
                    maze.grid[r][c].walls_state = _walls
            maze.seed = None
            maze.generate()
            solver = MazeSolver(maze)
            path = solver.shortest_path()
            show_path = False
            display_ascii(maze, path, show_path, wall_color)
            if path is not None:
                export_hex(maze, path, filename)
                print(f"Maze saved to {filename}")

        elif choice == "2":
            show_path = not show_path
            display_ascii(maze, path, show_path, wall_color)
            if show_path and path:
                print(f"Path: {''.join(path)}")
            elif path is None:
                print("No path found.")

        elif choice == "3":
            wall_color_idx = (wall_color_idx + 1) % len(WALL_COLORS)
            wall_color = WALL_COLORS[wall_color_idx][1]
            display_ascii(maze, path, show_path, wall_color)
            print(f"Wall color: {WALL_COLORS[wall_color_idx][0]}")

        elif choice == "4":
            print("Bye! (◕‿◕｡)")
            break

        else:
            print("Invalid choice.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Parse config, generate maze, export and display it."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        sys.exit(1)

    try:
        config = config_file(sys.argv[1])
        maze = MazeGenerator(config)
        maze.generate()

        solver = MazeSolver(maze)
        path = solver.shortest_path()

        if path is None:
            print("No path found between entry and exit.", file=sys.stderr)
            sys.exit(1)

        export_hex(maze, path, config.OUTPUTFILE)
        print(f"Maze exported to {config.OUTPUTFILE}")

        menu(maze, path, config.OUTPUTFILE)

    except Exception as error:  # noqa: BLE001
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

*This project has been created as part of the 42 curriculum by hgarcia2, jopaz-su.*

---

# A-Maze-ing 

A maze generator and solver written in Python 3.10+. The program reads a configuration file, generates a perfect (or imperfect) maze, displays it in the terminal with ANSI colors, and exports the result to a text file using a hexadecimal wall encoding.

---

## Description

A-Maze-ing generates grid-based mazes using a **recursive DFS (Depth-First Search / recursive backtracker)** algorithm. Each cell tracks which of its four walls (North, East, South, West) are intact using a bitmask. The generator carves passages between cells until every reachable cell has been visited, producing a perfect maze — one with exactly one path between any two points.

A hidden "42" pattern is embedded in the center of the maze as a set of fully walled cells, paying homage to the school. The program also computes the shortest path from entry to exit using BFS and exports the maze grid, coordinates, and path to an output file.

Key features:

- Reproducible generation via an optional seed
- Terminal ASCII rendering with ANSI wall colors
- Interactive menu: regenerate, show/hide path, cycle wall colors
- Hexadecimal output file compatible with automatic validators
- Reusable `MazeGenerator` class packaged as `mazegen`

---

## Instructions

### Requirements

- Python 3.10 or later
- `flake8` and `mypy` for linting (installed via `make install`)

### Installation

```bash
make install
```

This installs all dependencies listed in `requirements.txt` using pip.

### Run

```bash
make run
# equivalent to:
python3 a_maze_ing.py config.txt
```

You can pass any valid config file name:

```bash
python3 a_maze_ing.py my_config.txt
```

### Debug

```bash
make debug
```

Runs the program under Python's built-in debugger (`pdb`).

### Lint

```bash
make lint          # flake8 + mypy with standard flags
make lint-strict   # flake8 + mypy --strict
```

### Clean

```bash
make clean
```

Removes `__pycache__`, `.mypy_cache`, `.pytest_cache`, and compiled `.pyc` files.

---

## Configuration File Format

The program expects a plain text config file with one `KEY=VALUE` pair per line.  
Lines starting with `#` are treated as comments and ignored.  
All keys below are **mandatory**:

| Key           | Description                          | Example                  |
|---------------|--------------------------------------|--------------------------|
| `WIDTH`       | Maze width in cells                  | `WIDTH=15`               |
| `HEIGHT`      | Maze height in cells                 | `HEIGHT=15`              |
| `ENTRY`       | Entry coordinates as `x,y`          | `ENTRY=2,1`              |
| `EXIT`        | Exit coordinates as `x,y`           | `EXIT=13,14`             |
| `OUTPUT_FILE` | Path for the output file             | `OUTPUT_FILE=maze.txt`   |
| `PERFECT`     | Whether to generate a perfect maze   | `PERFECT=True`           |
| `SEED`        | Optional integer seed for reproducibility | `SEED=42`           |

Example `config.txt`:

```
# A-Maze-ing default configuration
WIDTH=15
HEIGHT=15
ENTRY=2,1
EXIT=13,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

Coordinates use `x,y` format where `x` is the column and `y` the row (0-indexed).

---

## Output File Format

The output file contains:

1. One row per line, each cell encoded as a single **hexadecimal digit** (uppercase).
2. Each hex digit is a 4-bit bitmask of the cell's walls:

| Bit | Direction |
|-----|-----------|
| 0 (LSB) | North |
| 1       | East  |
| 2       | South |
| 3       | West  |

A closed (present) wall sets the bit to `1`; an open passage sets it to `0`.  
Example: `A` (binary `1010`) means the East and West walls are closed.

3. After a blank line, three additional lines are appended:
   - Entry coordinates: `x,y`
   - Exit coordinates: `x,y`
   - Shortest path as a string of letters: `N`, `E`, `S`, `W`

All lines end with `\n`.

---

## Maze Generation Algorithm

The generator uses **recursive DFS (recursive backtracker)**:

1. Start from the entry cell and mark it as visited.
2. Shuffle the list of unvisited neighbors randomly.
3. For each unvisited neighbor not in the blocked set (the "42" pattern), carve a passage and recurse.
4. Backtrack when no unvisited neighbors remain.

This produces a **perfect maze** — a spanning tree of the grid with exactly one path between any two cells. The "42" pattern cells are excluded from the DFS so they remain as fully walled islands visible in the rendered output.

### Why this algorithm?

Recursive DFS was chosen for several reasons:

- **Simplicity**: the implementation is compact and easy to reason about.
- **Perfect mazes by construction**: DFS naturally produces a spanning tree, guaranteeing a single unique path between entry and exit.
- **Long, winding corridors**: DFS tends to create mazes with long passages before branching, which produces a more visually interesting and challenging layout than alternatives like Prim's or Kruskal's.
- **Easy seed support**: since all randomness flows through `random.shuffle`, fixing the seed with `random.seed()` makes the generation fully reproducible.

---

## Reusable Module — `mazegen`

The maze generation logic is packaged as a standalone Python package called **`mazegen`**, installable via pip.

### What is reusable

The `MazeGenerator` class in `maze_generator.py` (exposed through the `mazegen` package) encapsulates the full generation pipeline independently of the CLI, config parser, or display code. It gives direct access to:

- `grid`: a 2D list of `Cell` objects, each holding its wall bitmask
- `entry` / `exit`: coordinates as `(x, y)` tuples
- `blocked`: the set of cells reserved for the "42" pattern

### Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
# or from source:
pip install build
python -m build
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

### Basic usage example

```python
from mazegen.maze_generator import MazeGenerator
from mazegen.config_parser import ConfigMaze

# Build a config object manually
config = ConfigMaze()
config.WIDTH = 10
config.HEIGHT = 10
config.ENTRY = (0, 0)
config.EXIT = (9, 9)
config.SEED = 7
config.PERFECT = "True"
config.OUTPUTFILE = "output.txt"

# Instantiate and generate
gen = MazeGenerator(config)
gen.generate()

# Access the grid
cell = gen.cell_at(0, 0)
print(cell)           # Cell(0,0 walls=NSEW) — bitmask representation

# Check if a wall exists in a direction
from mazegen.cell import north, east, south, west
if cell.has_wall(east):
    print("East wall is closed")

# Iterate all cells
for row in gen.grid:
    for c in row:
        print(c.walls_state, end=" ")
    print()
```

### Passing custom parameters

All parameters are set via the `ConfigMaze` object before passing it to `MazeGenerator`:

| Parameter       | Type            | Description                        |
|-----------------|-----------------|------------------------------------|
| `WIDTH`         | `int`           | Number of columns                  |
| `HEIGHT`        | `int`           | Number of rows                     |
| `ENTRY`         | `tuple[int,int]`| Entry cell as `(x, y)`             |
| `EXIT`          | `tuple[int,int]`| Exit cell as `(x, y)`              |
| `SEED`          | `int \| None`   | RNG seed for reproducibility       |
| `PERFECT`       | `str`           | `"True"` to enforce a perfect maze |
| `OUTPUTFILE`    | `str`           | Path for the exported file         |

### Accessing the solution

The `MazeGenerator` itself generates the structure. To find the shortest path, use the `MazeSolver` class from the main module:

```python
from a_maze_ing import MazeSolver

solver = MazeSolver(gen)
path = solver.shortest_path()  # e.g. ['S', 'S', 'E', 'E', 'N', ...]
print("Path:", "".join(path) if path else "No path found")
```

---

## Team and Project Management

### Team members

| Member | Role |
|--------|------|
| `<login1>` | Maze generation algorithm, cell model, config parser |

### Planning

The project was planned in the following phases:

1. **Core data model** — `Cell` bitmask representation and direction constants.
2. **Generator** — DFS algorithm, "42" pattern, seed support.
3. **Config parser** — reading and validating `KEY=VALUE` files.
4. **Solver** — BFS shortest path.
5. **Display and menu** — ASCII terminal rendering with ANSI colors, interactive loop.
6. **Exporter** — hexadecimal output file.
7. **Packaging** — `pyproject.toml`, `mazegen` package, build and install flow.
8. **Linting and cleanup** — flake8, mypy, docstrings.

The main deviation from the original plan was that the "42" pattern integration required careful coordination between the DFS visited set and the blocked cell set to avoid disconnecting the maze.

### What worked well

- The bitmask encoding made wall checks and removals very clean.
- BFS for pathfinding was straightforward to layer on top of the generator.
- Keeping `MazeGenerator` independent of the config format made it easy to package separately.

### What could be improved

- The DFS is recursive, which can hit Python's stack limit for very large mazes; an iterative version would be more robust.
- The "42" pattern is hardcoded; a more general approach (any pattern as a bitmap) would be more flexible.
- Multiple generation algorithms (Prim's, Kruskal's, Wilson's) could be added as a bonus.

### Tools used

- **Python 3.10+** — core language
- **flake8** — style linting
- **mypy** — static type checking
- **pytest** — unit testing (not submitted)
- **setuptools / build** — package creation
- **Claude (Anthropic)** — used to review algorithm logic, suggest type hint improvements, and help draft docstrings. All generated suggestions were reviewed, tested, and understood before integration.

---

## Resources

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive backtracker — Think Labyrinth](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracker)
- [Graph theory and spanning trees — Khan Academy](https://www.khanacademy.org/computing/computer-science/algorithms)
- [Python `typing` module documentation](https://docs.python.org/3/library/typing.html)
- [mypy documentation](https://mypy.readthedocs.io/en/stable/)
- [flake8 documentation](https://flake8.pycqa.org/en/latest/)
- [Python packaging guide (setuptools)](https://setuptools.pypa.io/en/latest/)
- [PEP 257 — Docstring conventions](https://peps.python.org/pep-0257/)

### AI usage

Claude (Anthropic) was used during this project for the following tasks:

- Reviewing type hints and suggesting corrections to make code pass `mypy --strict`.
- Explaining edge cases in the DFS backtracker (e.g., handling blocked cells without disconnecting the graph).
- Drafting and reviewing docstrings following PEP 257 / Google style.
- Suggesting the BFS approach for the shortest path solver.

All AI-generated content was carefully reviewed, tested against the actual program behavior, and rewritten where necessary before being included. No code was copied blindly.
from dataclasses import dataclass, field

north: int = 0b0001
south: int = 0b0010
east: int = 0b0100
west: int = 0b1000
walls: int = north | south | east | west

directions: (dict[int, tuple[int, int]]) = {
    north: (-1, 0),
    south: (1, 0),
    east: (0, 1),
    west: (0, -1)
}

opposite_directions: (dict[int, int]) = {
    north: south,
    south: north,
    east: west,
    west: east
}

directions_letters: (dict[int, str]) = {
    north: "N",
    south: "S",
    east: "E",
    west: "W"
}

letters_directions: (dict[str, int]) = {
    "N": north,
    "S": south,
    "E": east,
    "W": west
}


@dataclass
class Cell:
    row: int
    col: int
    walls_state: int = field(default=walls)
# todas las paredes activas al inicio

    def has_wall(self, direction: int) -> bool:
        """Comprueba si existe una pared en la dirección dada."""
        return bool(self.walls_state & direction)

    def remove_wall(self, direction: int) -> None:
        """Elimina la pared en la dirección dada."""
        self.walls_state &= ~direction

    def add_wall(self, direction: int) -> None:
        """Añade la pared en la dirección dada."""
        self.walls_state |= direction

    def is_closed(self) -> bool:
        """Devuelve True si la celda tiene las 4 paredes."""
        return self.walls_state == walls

    def __repr__(self) -> str:
        active = [directions_letters[d] for d in (north, south, east, west)
                  if self.has_wall(d)]
        return f"Cell({self.row},{self.col} walls={''.join(active)})"

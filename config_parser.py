from typing import Optional
import sys


class ConfigMaze:
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    PERFECT: str
    OUTPUTFILE: str
    SEED: Optional[int]

    def __str__(self) -> str:
        return (f"ConfigMaze(WIDTH={self.WIDTH}, HEIGHT={self.HEIGHT}, "
                f"ENTRY={self.ENTRY}, EXIT={self.EXIT}, "
                f"OUTPUTFILE={self.OUTPUTFILE}, PERFECT={self.PERFECT}, "
                f"SEED={self.SEED})")


def coords_parser(key: str) -> tuple[int, int]:
    coords = key.split(",")

    if len(coords) != 2:
        raise ValueError(f"Invalid coordinates format: {key} should be in the"
                         "form 'x,y'.")

    try:
        coord1 = int(coords[0].strip())
        coord2 = int(coords[1].strip())
    except ValueError:
        raise ValueError(
            f"Invalid coordinates format: {key}."
            "Coordinates must be integers.")
    return (coord1, coord2)


def config_file(file_path: str) -> ConfigMaze:
    config = ConfigMaze()
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key_value = line.split("=")
                if len(key_value) != 2:
                    raise ValueError(f"Invalid configuration line: {line}")
                key, value = key_value[0].strip(), key_value[1].strip()
                if key == "WIDTH":
                    config.WIDTH = int(value)
                elif key == "HEIGHT":
                    config.HEIGHT = int(value)
                elif key == "ENTRY":
                    config.ENTRY = coords_parser(value)
                elif key == "EXIT":
                    config.EXIT = coords_parser(value)
                elif key == "OUTPUT_FILE":
                    config.OUTPUTFILE = value
                elif key == "PERFECT":
                    config.PERFECT = value
                elif key == "SEED":
                    config.SEED = int(value)
                else:
                    raise ValueError(f"Unknown configuration key: {key}")
    except FileNotFoundError:
        print(f"Configuration file not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    return config


if __name__ == "__main__":
    print(config_file("config.txt"))

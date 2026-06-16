from cell import east, south


class MazeExporter:
    def __init__(self, maze):
        self.maze = maze

    def to_ascii(self) -> str:
        maze = self.maze
        output = ""

        output += "+" + "---+" * maze.width + "\n"

        for r in range(maze.height):
            line1 = "|"
            line2 = "+"

            for c in range(maze.width):
                cell = maze.grid[r][c]

                line1 += "   "

                if cell.has_wall(east):
                    line1 += "|"
                else:
                    line1 += " "

                if cell.has_wall(south):
                    line2 += "---+"
                else:
                    line2 += "   +"

            output += line1 + "\n"
            output += line2 + "\n"

        return output

    def export_txt(self, filename: str):
        with open(filename, "w") as f:
            f.write(self.to_ascii())

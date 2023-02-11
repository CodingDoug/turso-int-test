class Table:
    header_line: str
    row_lines: list[str]

    def __init__(self, header_line: str, row_lines: list[str]):
        self.header_line = header_line
        self.row_lines = row_lines

    def find(self, name: str, row_line: str) -> str:
        start = self.header_line.find(name)
        space = self.header_line.find("  ", start)
        end = len(self.header_line)
        for i in range(space, len(self.header_line)):
            char = self.header_line[i]
            if char != " ":
                end = i
                break
        return row_line[start:end].strip()

def parse_table(raw: str):
    lines = raw.splitlines()
    header_line = lines.pop(0)
    return Table(header_line, lines)

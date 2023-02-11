from settings import DB_NAME, CLI
from output import Table, parse_table
import subprocess

def db_shell(db: str, sql: str) -> tuple[subprocess.CompletedProcess, Table | None]:
    cmd = CLI + ['db', 'shell', db, sql]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return result, None
    return result, parse_table(result.stdout)

if __name__ == '__main__':
    result, table = db_shell(DB_NAME, 'select 1, 2')
    if result.returncode == 0:
        line = table.row_lines[0]
        one = table.find('1', line)
        two = table.find('2', line)
        print(f'one: {one}')
        print(f'two: {two}')
    else:
        print(result.stderr, end='')

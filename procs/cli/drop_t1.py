from settings import DB_NAME
from ops.db_shell import db_shell

def drop_t1(db_name: str) -> None:
    result, table = db_shell(db_name, 'drop table if exists t1')

    print('Ran: ' + str(result.args))
    if result.returncode != 0:
        print(f'Return code {result.returncode}')
        print(result.stderr, end='')
        raise Exception()

    num_rows = len(table.row_lines)
    assert num_rows == 0, f'Expected 0 rows, got {num_rows}'

    len_header_line = len(table.header_line)
    assert len_header_line == 0, f'Expected 0 headers, got {len_header_line}'


import sys

if __name__ == '__main__':
    db_name: str
    if len(sys.argv) > 1:
        db_name = sys.argv[1]
    else:
        db_name = DB_NAME
    drop_t1(db_name)
    print('OK')

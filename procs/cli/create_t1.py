from settings import DB_NAME
from ops.db_shell import db_shell

class _Procedure():
    __db_name: str
    __num_rows = 10

    def __init__(self, db_name: str) -> None:
        self.__db_name = db_name

    def create_table(self) -> None:
        result, table = db_shell(self.__db_name, 'create table t1 (c1 text, c2 int)')
        print(f'Ran: {str(result.args)}')

        if result.returncode != 0:
            print(f'Return code {result.returncode}')
            print(result.stderr, end='')
            raise Exception()

        num_rows = len(table.row_lines)
        assert num_rows == 0, f'Expected 0 rows, got {num_rows}'

        len_headers = len(table.header_line)
        assert len_headers == 0, f'Expected 0 headers, got {table.header_line}'

    def insert_rows(self) -> None:
        for i in range(self.__num_rows):
            self._insert_row(i)

    def _insert_row(self, i: int) -> None:
        sql = f'insert into t1 values ("{i}", {i})'
        result, table = db_shell(self.__db_name, sql)
        print(f'Ran: {str(result.args)}')

        if result.returncode != 0:
            print(f'Return code {result.returncode}')
            print(result.stderr, end='')
            raise Exception()

        num_rows = len(table.row_lines)
        assert num_rows == 0, f'Expected 0 rows, got {num_rows}'

        len_header_line = len(table.header_line)
        assert len(table.header_line) == 0, f'Expected 0 headers, got {len_header_line}'

def create_t1(db_name: str) -> None:
    proc = _Procedure(db_name)
    proc.create_table()
    proc.insert_rows()


import sys

if __name__ == '__main__':
    db_name: str
    if len(sys.argv) > 1:
        db_name = sys.argv[1]
    else:
        db_name = DB_NAME
    create_t1(db_name)
    print('OK')

from settings import DB_NAME
from ops.db_shell import db_shell

class _Procedure():
    __db_name: str
    __num_rows = 10

    def __init__(self, db_name: str) -> None:
        self.__db_name = db_name

    def verify_rows(self):
        sql = 'select * from t1'
        result, table = db_shell(self.__db_name, sql)
        print(f'Ran: {str(result.args)}')

        if result.returncode != 0:
            print(f'Return code {result.returncode}')
            print(result.stderr, end='')
            raise Exception()

        num_rows = len(table.row_lines)
        assert num_rows == self.__num_rows, f'Expected {self.__num_rows} rows, got {num_rows}'

        for i in range(self.__num_rows):
            line = table.row_lines[i]
            c1 = table.find('C1', line)
            c2 = table.find('C2', line)
            assert c1 == str(i), f'Line {i} had unexpected data for c1: {c1}'
            assert c2 == str(i), f'Line {i} had unexpected data for c2: {c2}'

def verify_t1(db_name: str) -> None:
    proc = _Procedure(db_name)
    proc.verify_rows()


import sys

if __name__ == '__main__':
    db_name: str
    if len(sys.argv) > 1:
        db_name = sys.argv[1]
    else:
        db_name = DB_NAME
    verify_t1(db_name)
    print('OK')

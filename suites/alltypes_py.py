from settings import DB_NAME
from ops.db_show import db_show
from procs.py.create_alltypes import create_alltypes
from procs.py.drop_alltypes import drop_alltypes

def exec(db_name: str) -> None:
    result, db_show_result = db_show(db_name)
    print(f'Ran: {str(result.args)}')

    if result.check_returncode != 0:
        print(result.stderr, end='')
        raise Exception()

    db_url = db_show_result.url
    create_alltypes(db_url)
    drop_alltypes(db_url)

import sys

if __name__ == '__main__':
    exec(DB_NAME)
    print('OK')

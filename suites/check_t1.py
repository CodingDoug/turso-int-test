from settings import DB_NAME
from procs.cli.check_cli import check_cli
from procs.cli.create_t1 import create_t1
from procs.cli.verify_t1 import verify_t1
from procs.cli.drop_t1 import drop_t1

def exec(db_name: str) -> None:
    check_cli()
    create_t1(db_name)
    verify_t1(db_name)
    drop_t1(db_name)


import sys

if __name__ == '__main__':
    exec(DB_NAME)
    print('OK')

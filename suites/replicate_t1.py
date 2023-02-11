from settings import DB_NAME
from procs.cli.check_cli import check_cli
from procs.cli.create_t1 import create_t1
from procs.cli.create_replica import create_replica
from procs.cli.verify_t1 import verify_t1
from procs.cli.drop_t1 import drop_t1
from procs.cli.destroy_replica import destroy_replica

def exec(db_name: str, region: str) -> None:
    check_cli()
    create_t1(db_name)
    verify_t1(db_name)
    new_instance = create_replica(db_name, region)
    verify_t1(new_instance.url)
    drop_t1(db_name)
    destroy_replica(db_name, new_instance.name)


import sys

if __name__ == '__main__':
    region: str
    if len(sys.argv) > 1:
        region = sys.argv[1]
    else:
        print('Pass region for replica')
    exec(DB_NAME, region)
    print('OK')

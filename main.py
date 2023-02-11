import subprocess
from settings import *
import ops.db_create, ops.db_show

def main():
    raw, db_show = ops.db_show.db_show(DB_NAME)
    print(raw.args)
    print(raw.returncode)
    print(raw.stdout)
    print(raw.stderr)
    print(db_show.name)

if __name__ == '__main__':
    main()

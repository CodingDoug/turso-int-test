from settings import DB_NAME
from ops.version import version

def check_cli() -> None:
    result, v = version()
    print(f'Ran: {str(result.args)}')

    if result.returncode != 0:
        print(f'Return code {result.returncode}')
        print(result.stderr, end='')
        raise Exception()

    assert v != None, 'Turso CLI version not found'
    print(f'Turso CLI version {v}')


import sys

if __name__ == '__main__':
    check_cli()
    print('OK')

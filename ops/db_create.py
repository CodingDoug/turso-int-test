from settings import DB_NAME, CLI
import subprocess

def db_create(db_name: str) -> subprocess.CompletedProcess:
    cmd = CLI + ['db', 'create', db_name]
    return subprocess.run(cmd, capture_output=True, text=True)

if __name__ == '__main__':
    result = db_create(DB_NAME)
    if result.returncode == 0:
        print(result.stdout, end='')
    else:
        print(result.stderr, end='')

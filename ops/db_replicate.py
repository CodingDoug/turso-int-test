from settings import DB_NAME, CLI
import subprocess

def db_replicate(db_name: str, region: str) -> subprocess.CompletedProcess:
    cmd = CLI + ['db', 'replicate', db_name, region]
    return subprocess.run(cmd, capture_output=True, text=True)

if __name__ == '__main__':
    result = db_replicate(DB_NAME, 'nrt')
    if result.returncode == 0:
        print(result.stdout, end='')
    else:
        print(result.stderr, end='')

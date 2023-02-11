from settings import DB_NAME, CLI
import subprocess

def db_destroy_region(db_name: str, region: str) -> subprocess.CompletedProcess:
    cmd = CLI + ['db', 'destroy', db_name, '--region', region]
    return subprocess.run(cmd, capture_output=True, text=True)

if __name__ == '__main__':
    result = db_destroy_region(DB_NAME, instance='nrt')
    if result.returncode == 0:
        print(result.stdout, end='')
    else:
        print(result.stderr, end='')

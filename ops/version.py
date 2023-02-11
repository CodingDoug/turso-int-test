from settings import CLI
import subprocess

def version() -> tuple[subprocess.CompletedProcess, str | None]:
    cmd = CLI + ['--version']
    result = subprocess.run(cmd, capture_output=True, text=True)
    version: str | None
    if result.stdout.startswith('turso version v'):
        version = result.stdout.removeprefix('turso version v').strip()
    return result, version

if __name__ == '__main__':
    result, version = version()
    if result.returncode == 0:
        if version != None:
            print('Version: ' + version)
        else:
            print('Version not detected')
            print(result.stdout, end='')
    else:
        print(result.stderr, end='')

from settings import DB_NAME, CLI
import subprocess

class Instance():
    name: str
    type: str
    region: str
    url: str

    def __init__(self) -> None:
        self.name = None
        self.type = None
        self.region = None
        self.url = None

class DbShowResult():
    name: str
    url: str
    id: str
    regions: list[str]
    instances: list[Instance]

    def __init__(self) -> None:
        self.name = None
        self.url = None
        self.regions = []
        self.instances = []

def db_show(db_name: str) -> tuple[subprocess.CompletedProcess, DbShowResult | None]:
    cmd = CLI + ['db', 'show', db_name]
    raw_result = subprocess.run(cmd, capture_output=True, text=True)
    if raw_result.returncode == 0:
        db_show_result = DbShowResult()
        lines = raw_result.stdout.splitlines()
        header_line: str
        for line in lines:
            if line.startswith('Name:'):
                db_show_result.name = line[line.index(':')+1:].strip()
            elif line.startswith('URL:'):
                db_show_result.url = line[line.index(':')+1:].strip()
            elif line.startswith('ID:'):
                db_show_result.id = line[line.index(':')+1:].strip()
            elif line.startswith('Regions:'):
                db_show_result.regions = line[line.index(':')+1:].strip().split(', ')
            elif line.startswith('NAME '):
                header_line = line
            elif (len(line) == 0):
                # skip empty lines
                pass
            elif line.startswith('Database Instances:'):
                pass
            else:
                if header_line == None:
                    pass
                # print(line)
                instance = Instance()
                instance.name = _find_value('NAME', header_line, line)
                instance.type = _find_value('TYPE', header_line, line)
                instance.region = _find_value('REGION', header_line, line)
                instance.url = _find_value('URL', header_line, line)
                # print(instance.__dict__)
                db_show_result.instances.append(instance)
        return raw_result, db_show_result
    return raw_result, None

def _find_value(name: str, header_line: str, line: str) -> str:
    start = header_line.find(name)
    space = header_line.find('  ', start)
    end = len(header_line)
    for i in range(space, len(header_line)):
        char = header_line[i]
        if char != ' ':
            end = i
            break
    # print(header_line[start:end])
    return line[start:end].strip()


import jsonpickle
import json

if __name__ == '__main__':
    raw_result, db_show_result = db_show(DB_NAME)
    if raw_result.returncode == 0:
        # print(dir(db_show_result))
        print(json.dumps(json.loads(jsonpickle.encode(db_show_result))))
        print(json.dumps(json.loads(jsonpickle.encode(db_show_result.instances))))
        # print(vars(db_show_result))
        # print(db_show_result.instances)
        # print(db_show_result.__dir__())
    else:
        print(raw_result.stderr, end='')

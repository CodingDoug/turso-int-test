from settings import DB_NAME
from ops.db_replicate import db_replicate
from ops.db_show import Instance, db_show

class _Procedure():
    __db_name: str
    __region: str
    __instances: dict[str, Instance] = {}
    new_instance: Instance

    def __init__(self, db_name: str, region: str) -> None:
        self.__db_name = db_name
        self.__region = region

    def pre_show(self) -> None:
        result, db_show_result = db_show(self.__db_name)
        print(f'Ran: {str(result.args)}')

        if result.returncode != 0:
            print(f'Return code {result.returncode}')
            print(result.stderr, end='')
            raise Exception()

        for instance in db_show_result.instances:
            self.__instances[instance.name] = instance

    def replicate(self) -> None:
        result = db_replicate(self.__db_name, self.__region)
        print(f'Ran: {str(result.args)}')

        if result.returncode != 0:
            print(f'Return code {result.returncode}')
            print(result.stderr, end='')
            raise Exception()

    def post_show(self) -> None:
        result, db_show_result = db_show(self.__db_name)
        print(f'Ran: {str(result.args)}')

        if result.returncode != 0:
            print(f'Return code {result.returncode}')
            print(result.stderr, end='')
            raise Exception()

        instances = {}
        for instance in db_show_result.instances:
            instances[instance.name] = instance

        if len(instances) != len(self.__instances) + 1:
            print('Number of instances did not increment')
            print(result.stdout, end='')
            raise Exception()

        new_name = (instances.keys() - self.__instances.keys()).pop()
        self.new_instance = instances[new_name]

def create_replica(db_name: str, region: str) -> Instance:
    proc = _Procedure(db_name, region)
    proc.pre_show()
    proc.replicate()
    proc.post_show()
    return proc.new_instance

import sys

if __name__ == '__main__':
    db_name: str
    region: str
    if len(sys.argv) > 2:
        db_name = sys.argv[1]
        region = sys.argv[2]
    else:
        print('Pass db_name and region')
    instance = create_replica(db_name, region)
    print(f'New instance: {instance.name}')
    print('OK')

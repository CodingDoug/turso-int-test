from settings import DB_NAME
from ops.db_destroy_instance import db_destroy_instance
from ops.db_show import Instance, db_show

class _Procedure():
    __db_name: str
    __instance: str
    __starting_instances: dict[str, Instance] = {}

    def __init__(self, db_name: str, instance: str) -> None:
        self.__db_name = db_name
        self.__instance = instance

    def pre_show(self) -> None:
        result, db_show_result = db_show(self.__db_name)

        if result.returncode != 0:
            print(f'Return code {result.returncode}')
            print(result.stderr, end='')
            raise Exception()

        for instance in db_show_result.instances:
            self.__starting_instances[instance.name] = instance

    def destroy(self) -> None:
        result = db_destroy_instance(self.__db_name, self.__instance)
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

        if self.__instance in instances:
            print(f'Instance {self.__instance} still present')
            print(result.stdout, end='')
            raise Exception()

def destroy_replica(db_name: str, instance: str) -> None:
    proc = _Procedure(db_name, instance)
    proc.pre_show()
    proc.destroy()
    proc.post_show()

import sys

if __name__ == '__main__':
    db_name: str
    instance: str
    if len(sys.argv) > 2:
        db_name = sys.argv[1]
        instance = sys.argv[2]
    else:
        print('Pass db_name and instance')
    destroy_replica(db_name, instance)
    print('OK')

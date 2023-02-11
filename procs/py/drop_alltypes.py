import asyncio
import libsql_client

class _Procedure:
    _db_url: str
    _client: libsql_client.Client

    def __init__(self, db_url: str) -> None:
        self._db_url = db_url
        self._client = libsql_client.Client(self._db_url)

    async def drop_alltypes(self) -> None:
        await self._client.execute('drop table alltypes')

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def close(self) -> None:
        await self._client.close()


async def _drop_alltypes(db_url: str) -> None:
    async with _Procedure(db_url) as proc:
        await proc.drop_alltypes()

def drop_alltypes(db_name: str) -> None:
    asyncio.run(_drop_alltypes(db_url))


import sys

if __name__ == '__main__':
    db_url: str
    if len(sys.argv) > 1:
        db_url = sys.argv[1]
    else:
        sys.exit('Pass database url')
    drop_alltypes(db_url)
    print('OK')

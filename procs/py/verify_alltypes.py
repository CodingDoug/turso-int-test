import asyncio
import libsql_client

class _Procedure():
    _db_url: str
    _client: libsql_client.Client

    def __init__(self, db_url: str) -> None:
        self._db_url = db_url
        self._client = libsql_client.Client(self._db_url)

    async def verify_alltypes(self) -> None:
        result = await self._client.execute('select * from alltypes')

        num_columns = len(result.columns)
        assert num_columns == 4, f'ResultSet had {num_columns} columns, expected 4'

        num_rows = len(result.rows)
        assert num_rows == 2, f'ResultSet had {num_rows} rows, expected 2'

        row = result.rows[0]
        assert len(row) == 4, f'row had {len(row)} values, expected 4'

        await self._verify_row0(row)

        row = result.rows[1]
        assert len(row) == 4, f'row had {len(row)} values, expected 4'

        await self._verify_row1(row)

    async def _verify_row0(self, row: libsql_client.Row) -> None:
        t = row['t']
        assert t == "text", f't value was {t}, expected "text"'

        i = row['i']
        assert i == 99, f'i value was {i}, expected 99'

        r = row['r']
        assert r == 3.14, f'r value was {r}, expected 3.14'

        b = row['b']
        assert b == bytes([0, 1, 2, 3]), f'b value was {b}, expected [0, 1, 2, 3]'

    async def _verify_row1(self, row: libsql_client.Row) -> None:
        t = row[0]
        assert t == None, f't value was {t}, expected None'

        i = row[1]
        assert i == None, f'i value was {i}, expected None'

        r = row[2]
        assert r == None, f'r value was {r}, expected None'

        b = row[3]
        assert b == None, f'b value was {b}, expected None'

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def close(self) -> None:
        await self._client.close()


async def _verify_alltypes(db_url: str) -> None:
    async with _Procedure(db_url) as proc:
        await proc.verify_alltypes()

def verify_alltypes(db_url: str) -> None:
    asyncio.run(_verify_alltypes(db_url))


import sys

if __name__ == '__main__':
    db_url: str
    if len(sys.argv) > 1:
        db_url = sys.argv[1]
    else:
        sys.exit('Pass database url')
    verify_alltypes(db_url)
    print('OK')

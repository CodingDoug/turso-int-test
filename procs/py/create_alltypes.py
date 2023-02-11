import asyncio
import libsql_client

class _Procedure:
    _db_url: str
    _client: libsql_client.Client

    def __init__(self, db_url: str) -> None:
        self._db_url = db_url
        self._client = libsql_client.Client(self._db_url)

    async def create_alltypes(self) -> None:
        rs = await self._client.execute('create table alltypes (t text, i integer, r real, b blob)')

        num_columns = len(rs.columns)
        assert len(rs.columns) == 0, f'ResultSet had {num_columns} columns, expected 0'

        num_rows = len(rs.rows)
        assert len(rs.rows) == 0, f'ResultSet had {num_rows} rows, expected 0'

    async def populate_alltypes(self) -> None:
        await self._populate_row0()
        await self._populate_row1()

    async def _populate_row0(self) -> None:
        rs = await self._client.execute(
            'insert into alltypes values (?, ?, ?, ?)',
            [ 'text', 99, 3.14, bytes([0, 1, 2, 3]) ]
        )

        num_columns = len(rs.columns)
        assert len(rs.columns) == 0, f'ResultSet had {num_columns} columns, expected 0'

        num_rows = len(rs.rows)
        assert len(rs.rows) == 0, f'ResultSet had {num_rows} rows, expected 0'

    async def _populate_row1(self) -> None:
        rs = await self._client.execute(
            'insert into alltypes values (?, ?, ?, ?)',
            [ None, None, None, None ]
        )

        num_columns = len(rs.columns)
        assert len(rs.columns) == 0, f'ResultSet had {num_columns} columns, expected 0'

        num_rows = len(rs.rows)
        assert len(rs.rows) == 0, f'ResultSet had {num_rows} rows, expected 0'

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def close(self) -> None:
        await self._client.close()


async def _create_alltypes(db_url: str) -> None:
    async with _Procedure(db_url) as proc:
        await proc.create_alltypes()
        await proc.populate_alltypes()

def create_alltypes(db_url: str) -> None:
    asyncio.run(_create_alltypes(db_url))


import sys

if __name__ == '__main__':
    db_url: str
    if len(sys.argv) > 1:
        db_url = sys.argv[1]
    else:
        sys.exit('Pass database url')
    create_alltypes(db_url)
    print('OK')

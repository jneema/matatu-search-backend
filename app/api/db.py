import os
import asyncpg
from typing import AsyncGenerator, cast
from dotenv import load_dotenv

_pool: asyncpg.Pool | None = None
load_dotenv()

async def init_pool() -> None:
    global _pool
    dsn = os.environ["DATABASE_URL"]
    _pool = await asyncpg.create_pool(dsn, min_size=2, max_size=10)


async def close_pool() -> None:
    global _pool
    if _pool:
        await _pool.close()


async def get_conn() -> AsyncGenerator[asyncpg.Connection, None]:
    if _pool is None:
        raise RuntimeError("DB pool not initialized")

    async with _pool.acquire() as conn:
        yield cast(asyncpg.Connection, conn)
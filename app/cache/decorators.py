import msgpack
from app.db.redis import get_redis_client


async def cache_get(key: str) -> dict | None:
    redis = await get_redis_client()
    data = await redis.get(key)
    if data:
        return msgpack.unpackb(data, raw=False)
    return None


async def cache_set(key: str, value: dict, ttl_seconds: int = 120) -> None:
    redis = await get_redis_client()
    await redis.setex(key, ttl_seconds, msgpack.packb(value, use_bin_type=True))


async def cache_delete(key: str) -> None:
    redis = await get_redis_client()
    await redis.delete(key)
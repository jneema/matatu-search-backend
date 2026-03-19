import msgpack
from app.db.redis import get_redis_client


async def cache_get(key: str) -> dict | None:
    try:
        redis = await get_redis_client()
        data = await redis.get(key)
        if data:
            return msgpack.unpackb(data, raw=False)
    except Exception:
        pass
    return None


async def cache_set(key: str, value: dict, ttl_seconds: int = 120) -> None:
    try:
        redis = await get_redis_client()
        packed = msgpack.packb(value, use_bin_type=True)
        await redis.setex(key, ttl_seconds, packed)
    except Exception:
        pass


async def cache_delete(key: str) -> None:
    try:
        redis = await get_redis_client()
        await redis.delete(key)
    except Exception:
        pass


async def cache_delete_pattern(pattern: str) -> None:
    try:
        redis = await get_redis_client()
        keys = await redis.keys(pattern)
        if keys:
            await redis.delete(*keys)
    except Exception:
        pass
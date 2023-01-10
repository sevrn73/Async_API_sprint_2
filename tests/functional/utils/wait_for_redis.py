import asyncio
import logging

import aioredis
import backoff

from settings import TEST_SETTINGS


logger = logging.getLogger("tests")

def backoff_handler(details):
    logger.info("Redis is unavailable - sleeping")

@backoff.on_exception(
    backoff.expo,
    (ConnectionError,),
    on_backoff=backoff_handler,
    max_time=60,
)
async def wait_for_redis():
    redis_client = await aioredis.create_redis_pool(
        (TEST_SETTINGS.redis_host, TEST_SETTINGS.redis_port), minsize=10, maxsize=20
    )
    ping = await redis_client.ping()
    if ping:
        return ping
    raise Exception


if __name__ == "__main__":
    asyncio.run(wait_for_redis())

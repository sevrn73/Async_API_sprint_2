import asyncio
import aioredis
import logging

from functional.utils.settings import TEST_SETTINGS

logger = logging.getLogger('tests')

async def wait_for_redis():
    redis_client = await aioredis.create_redis_pool((TEST_SETTINGS.redis_host, TEST_SETTINGS.redis_port), minsize=10, maxsize=20)
    response = await redis_client.ping()
    while not response:
        await asyncio.sleep(2)
        print('Redis is unavailable - sleeping')
        logger.info('Redis is unavailable - sleeping')
        response = await redis_client.ping()


if __name__ == '__main__':
    asyncio.run(wait_for_redis())


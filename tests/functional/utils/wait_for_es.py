import asyncio
import logging

import backoff
from elasticsearch import AsyncElasticsearch

from settings import TEST_SETTINGS


logger = logging.getLogger("tests")

def backoff_handler(details):
    logger.info("Elastic is unavailable - sleeping")

@backoff.on_exception(
    backoff.expo,
    (ConnectionError,),
    on_backoff=backoff_handler,
    max_time=60,
)
async def wait_for_es():
    es_client = AsyncElasticsearch(hosts=[TEST_SETTINGS.es_host,], validate_cert=False, use_ssl=False)
    ping = await es_client.ping()
    if ping:
        return ping
    raise Exception

if __name__ == "__main__":
    asyncio.run(wait_for_es())

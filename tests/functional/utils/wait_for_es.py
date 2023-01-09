import asyncio
from elasticsearch import AsyncElasticsearch
import logging

from settings import TEST_SETTINGS

logger = logging.getLogger('tests')

async def wait_for_es():
    es_client = AsyncElasticsearch(hosts=[TEST_SETTINGS.es_host, ], validate_cert=False, use_ssl=False)
    response = await es_client.ping()
    while not response:
        print("elastic не отвечает")
        await asyncio.sleep(2)
        print('Elastic is unavailable - sleeping')
        logger.info('Elastic is unavailable - sleeping')
        response = await es_client.ping()
    await es_client.close()



if __name__ == '__main__':
    asyncio.run(wait_for_es())

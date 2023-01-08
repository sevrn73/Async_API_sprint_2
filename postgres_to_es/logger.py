import logging
import sys

logging.basicConfig(
    filename='log.txt',
)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logger = logging.getLogger('loader')

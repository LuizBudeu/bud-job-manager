import logging
import pathlib


BASE_DIR = pathlib.Path(__file__).parent

LOGS_DIR = BASE_DIR / 'logs'


logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    # filename=LOGS_DIR / 'logs.log',
)

import logging
import os

if os.getenv('LOGGING_LEVEL'):
    LOGGING_LEVEL = getattr(logging, os.getenv('LOGGING_LEVEL'))
else:
    LOGGING_LEVEL = logging.INFO

# Constants:
LOG_FORMAT = '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "filename":  "%(filename)s", "msg": "%(message)s"}'

DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT', 5432))
DB_NAME = os.getenv('DB_NAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_USER = os.getenv('DB_USER')
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, scoped_session

import os

basedir = os.path.abspath(os.path.dirname(__file__))
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT', 5432))
DB_NAME = os.getenv('DB_NAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_USER = os.getenv('DB_USER')


class Config(object):
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# SQLALCHEMY_DATABASE_URL = f'postgresql://{env.DB_USER}:{env.DB_PASSWORD}@{env.DB_HOST}:{env.DB_PORT}/{env.DB_NAME}'

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,
# )
#
# session_factory = sessionmaker(bind=engine, autocommit=False, autoflush=True)
#
# SessionLocal = scoped_session(session_factory)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.configuration import env as config

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=True)
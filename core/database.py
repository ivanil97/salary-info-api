import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database

from core.settings import settings

DB_USER = settings.db_user
DB_PASS = settings.db_password
DB_HOST = settings.db_host
DB_NAME = settings.db_name
DB_PORT = settings.db_port

URL_DATABASE = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
TESTING_URL_DATABASE = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/test_{DB_NAME}'

if not database_exists(TESTING_URL_DATABASE):
    create_database(TESTING_URL_DATABASE)

engine = create_engine(URL_DATABASE)
testing_engine = create_engine(TESTING_URL_DATABASE)

if "pytest" in sys.argv[0]:
    Session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=testing_engine)
else:
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(engine)

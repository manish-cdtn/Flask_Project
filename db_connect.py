from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Config

_DB_SESSION = None
_DB_ENGINE_SESSION = None

env_vars = dotenv_values()
def get_db_engine_session():
    url_str = f'postgresql://postgres:postgres@localhost:5432/postgres'
    _DB_ENGINE_SESSION = create_engine(url_str, connect_args={'options': '-csearch_path={}'.format('dbo')})

    return _DB_ENGINE_SESSION


def get_db_session():
    """
    Returns DB session.
    """
    global _DB_SESSION
    if _DB_SESSION is None:
        session = sessionmaker(bind=get_db_engine_session())
        _DB_SESSION = session()
    return _DB_SESSION

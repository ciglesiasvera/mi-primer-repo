from sqlalchemy import create_engine
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

def get_engine():
    url = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    return create_engine(url)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import time
from .config import settings


# Database connection with retry logic
def create_db_engine():
    SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{settings.database_user}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"

    max_retries = 5
    retry_delay = 5  # seconds
    retry_count = 0

    while retry_count < max_retries:
        try:
            engine = create_engine(SQLALCHEMY_DATABASE_URL)
            # Test the connection
            with engine.connect() as connection:
                pass
            print("Successfully connected to the database!")
            return engine
        except OperationalError as e:
            retry_count += 1
            print(f"Connection failed (attempt {retry_count}/{max_retries}): {e}")
            if retry_count < max_retries:
                time.sleep(retry_delay)

    raise Exception("Could not connect to the database after multiple attempts")


engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
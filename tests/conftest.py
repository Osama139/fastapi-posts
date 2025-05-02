from fastapi.testclient import TestClient
from app.main import app
import pytest
from app import models, database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import time
from app.oauth2 import create_access_token
from app.config import settings

# Database connection with retry logic
def create_db_engine():
    SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{settings.database_user}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}_test"

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
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[database.get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture()
def test_user(client):
    user_data = {"name": "osama", "email": "osama@fakeemail.com", "password": "osama1399"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture()
def token(test_user):
    return create_access_token({'user_id': test_user['id']})

@pytest.fixture()
def authorized_client(client, token):
    client.headers["Authorization"] = f"Bearer {token}"
    return client

@pytest.fixture()
def test_posts(test_user, session):
    posts_data = [
        {"title":"some title1","content":"some content1","published":False, "user_id": test_user["id"]},
        {"title": "some title2", "content": "some content2", "published": True, "user_id": test_user["id"]},
        {"title": "some title3", "content": "some content3", "published": False, "user_id": test_user["id"]}
    ]
    for post in posts_data:
        session.add(models.Post(**post))
    session.commit()

    posts = session.query(models.Post).all()
    return posts
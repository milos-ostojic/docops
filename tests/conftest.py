import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from docops.db import Base, get_session
from docops.main import app

TEST_DATABASE_URL = "postgresql+psycopg://docops:docops@localhost:5433/docops_test"

test_engine = create_engine(TEST_DATABASE_URL)
TestSession = sessionmaker(bind=test_engine)


def override_get_session():
    with TestSession() as session:
        yield session


@pytest.fixture
def client():
    Base.metadata.create_all(test_engine)
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    Base.metadata.drop_all(test_engine)

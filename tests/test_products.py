from fastapi.testclient import TestClient
import pytest
from sqlmodel import create_engine, Session, SQLModel
from backend.main import app
from backend.database import get_session
from tests.utils import cleanup_database

# Create a persistent in-memory database engine for testing
memory_engine = create_engine(
    "sqlite:///./test_products.db",
    echo=True,
    connect_args={"check_same_thread": False}
)

# Make sure tables are created before running any test
SQLModel.metadata.create_all(memory_engine)

# Dependency override for using test database in API routes
def get_test_session():
    with Session(memory_engine) as session:
        yield session

app.dependency_overrides[get_session] = get_test_session

# Create a test client for the FastAPI application
client = TestClient(app)

def test_create_product():
    """
    Tests the creation of a product via the API using an in-memory database.

    Steps:
        1. Sends a POST request to create a product with specific attributes.
        2. Asserts that the response status code is 200.
        3. Validates that the returned product data matches the input data.
    """
    response = client.post("/api/products/create/", json={
        "name": "Test Product",
        "short_description": "Short",
        "product_description": "Long",
        "price": 9.99,
        "stock": {"quantity": 100}
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["stock"]["quantity"] == 100

def test_get_product_by_id():
    """
    Tests retrieving a product by its ID via the API using an in-memory database.

    Steps:
        1. Creates a product using a POST request.
        2. Extracts the product ID from the response.
        3. Sends a GET request to retrieve the product by its ID.
        4. Asserts that the response status code is 200.
        5. Validates that the retrieved product ID matches the created product ID.
    """
    create_response = client.post("/api/products/create/", json={
        "name": "Entry",
        "short_description": "Test",
        "product_description": "Description",
        "price": 1.99,
        "stock": {"quantity": 1}
    })
    assert create_response.status_code == 200
    product_id = create_response.json()["id"]

    get_response = client.get(f"/api/products/{product_id}/")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == product_id
    assert get_response.json()["stock"]["quantity"] == 1

@pytest.fixture(scope="session", autouse=True)
def cleanup_db_at_end():
    yield
    cleanup_database(memory_engine, "test_products.db")

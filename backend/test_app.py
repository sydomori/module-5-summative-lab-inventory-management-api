import pytest
from app import app, items, Item

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        items.clear()  # Clear items after each test to ensure isolation

def test_get_items_empty(client):
    response = client.get('/api/inventory')
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_items_with_items(client):
    # Add a test item
    test_item = Item(id=1, barcode="1234567890123", name="Test Product", brand="Test Brand", ingredients="Test Ingredients", in_stock=10, price=5.99)
    items.append(test_item)

    response = client.get('/api/inventory')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['name'] == "Test Product"
    assert data[0]['barcode'] == "1234567890123"
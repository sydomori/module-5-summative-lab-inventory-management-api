import pytest
from app import app, items, Item
from unittest.mock import patch

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

#get_item tests
def test_get_one_item_found(client):
    # Add a test item
    test_item = Item(id=1, barcode="1234567890123", name="Test Product", brand="Test Brand", ingredients="Test Ingredients", in_stock=10, price=5.99)
    items.append(test_item)

    response = client.get('/api/inventory/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == 1
    assert data['name'] == "Test Product"

def test_get_one_item_not_found(client):
    response = client.get('/api/inventory/999')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data

#add_item tests
def test_add_item(client):
    fake_product_data = {
        "name": "Test Product",
        "brand": "Test Brand",
        "ingredients": "Test Ingredient 1, Test Ingredient 2"
    }

    with patch('app.fetch_openfoodfacts_data', return_value=fake_product_data):
        response = client.post('/api/inventory', json={
            "barcode": "1234567890123",
            "in_stock": 10,
            "price": 5.99
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == "Test Product"
        assert data['brand'] == "Test Brand"
        assert data['barcode'] == "1234567890123"
        assert data['in_stock'] == 10
        assert data['price'] == 5.99     

#add item tests for error cases
def test_add_item_product_not_found(client):
    with patch('app.fetch_openfoodfacts_data', return_value=None):
        response = client.post('/api/inventory', json={
            "barcode": "0000000000000",
            "in_stock": 5,
            "price": 3.99
        })
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data

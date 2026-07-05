from flask import Flask, jsonify, request
from flask_cors import CORS
import requests


app = Flask(__name__)
CORS(app) #allow cross-origin requests

# Item class to define the structure of an item in the inventory
#to_dict method to convert the item object to a dictionary for JSON serialization
class Item:
    def __init__(self, id, barcode, name, brand, ingredients, in_stock, price):
        self.id = id
        self.barcode = barcode
        self.name = name
        self.brand = brand
        self.ingredients = ingredients
        self.in_stock = in_stock
        self.price = price

    def to_dict(self):
        return {
            'id': self.id,
            'barcode': self.barcode,
            'name': self.name,
            'brand': self.brand,
            'ingredients': self.ingredients,
            'in_stock': self.in_stock,
            'price': self.price
        }

# Sample items for demonstration purposes
items = [
    Item(1, "1234567890123", "Sample Product 1", "Brand A", "Ingredient 1, Ingredient 2", 50, 9.99),
    Item(2, "9876543210987", "Sample Product 2", "Brand B", "Ingredient 3, Ingredient 4", 0, 14.99)
]

def fetch_openfoodfacts_data(barcode):
    # Fetch product data from OpenFoodFacts API using the provided barcode
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        return None
    
    # Parse the JSON response
    data = response.json()

    # Check if the product was found and return relevant information
    # status 1 indicates that the product was found, while status 0 indicates that it was not found
    if data.get('status') != 1:
        return None
    
    # Extract relevant product information from the response
    product = data.get('product', {})
    return {
        "name" : product.get("product_name", "Unknown Product"),
        "brand" : product.get("brands", "Unknown Brand"),
        "ingredients" : product.get("ingredients_text", "Unknown Ingredients")
    }

@app.route('/api/inventory', methods=['GET'])
def get_items():
    return jsonify([item.to_dict() for item in items]), 200

@app.route('/api/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((i for i in items if i.id == item_id), None)
    if item:
        return jsonify(item.to_dict()), 200
    return jsonify({"error": "Item not found"}), 400

@app.route('/api/inventory', methods=['POST'])
def add_item():
    data = request.get_json()
    barcode = data.get('barcode')

    if not barcode:
        return jsonify({"error": "Barcode is required"}), 400
    
    product_data = fetch_openfoodfacts_data(barcode)

    if product_data is None:
        return jsonify({"error": "Product not found in OpenFoodFacts"}), 404
    
    new_id = max(item.id for item in items) + 1 if items else 1
    new_item = Item(
        id=new_id,
        barcode=barcode,
        name=product_data["name"],
        brand=product_data["brand"],
        ingredients=product_data["ingredients"],
        in_stock=data.get('in_stock',0),
        price=data.get('price', 0.0)
    )
    items.append(new_item)
    return jsonify(new_item.to_dict()), 201

@app.route('/api/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    data = request.get_json()
    item = next((i for i in items if i.id == item_id), None)
    if item:
        item.name  = data.get('name', item.name)
        item.brand = data.get('brand', item.brand)
        item.ingredients = data.get('ingredients', item.ingredients)
        item.in_stock = data.get('in_stock', item.in_stock)
        item.price = data.get('price', item.price)
        return jsonify(item.to_dict()), 200
    else:
        return jsonify({"error": "Item not found"}), 404

@app.route('/api/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    item = next((i for i in items if i.id == item_id), None)
    if item:
        items = [i for i in items if i.id != item_id]
        return jsonify({"message": "Item deleted"}), 200
    else:
        return jsonify({"error": "Item not found"}), 404



if __name__ == '__main__':
    app.run(debug=True, port=5000)
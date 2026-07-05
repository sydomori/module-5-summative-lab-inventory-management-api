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
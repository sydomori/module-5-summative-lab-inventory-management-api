from flask import Flask, jsonify, request
from flask_cors import CORS


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

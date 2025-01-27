from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/ecommerce_db")
client = MongoClient(MONGO_URI)
db = client.ecommerce
products_collection = db.products
users_collection = db.users
orders_collection = db.orders

@app.route("/")
def home():
    return "E-commerce API is running!"

@app.route("/products", methods=["POST"])
def add_product():
    data = request.json
    product = {
        "name": data["name"],
        "price": data["price"],
        "description": data["description"],
        "category": data["category"],
        "stock": data["stock"],
    }
    product_id = products_collection.insert_one(product).inserted_id
    return jsonify({"message": "Product added", "product_id": str(product_id)}), 201
    
@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product_id = ObjectId(product_id)
    except Exception as e:
        return jsonify({"message": "Invalid product ID format"}), 400

    product = products_collection.find_one({"_id": product_id})
    
    if product:
        product["_id"] = str(product["_id"]) 
        return jsonify(product), 200
    else:
        return jsonify({"message": "Product not found"}), 404



@app.route("/products", methods=["GET"])
def get_products():
    products = list(products_collection.find())
    for product in products:
        product["_id"] = str(product["_id"])
    return jsonify(products), 200

@app.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):

    try:
        product_id = ObjectId(product_id)
    except Exception as e:
        return jsonify({"message": "Invalid product ID format"}), 400

    data = request.get_json()

    result = db.products.update_one(
        {"_id": product_id}, 
        {"$set": data}  
    )

    if result.matched_count > 0:
        return jsonify({"message": "Product updated successfully"}), 200
    else:
        return jsonify({"message": "Product not found"}), 404

@app.route("/users/register", methods=["POST"])
def register_user():
    data = request.json
    hashed_password = generate_password_hash(data["password"])
    user = {
        "name": data["name"],
        "email": data["email"],
        "password": hashed_password,
        "role": "customer",
    }
    user_id = users_collection.insert_one(user).inserted_id
    return jsonify({"message": "User registered", "user_id": str(user_id)}), 201

@app.route("/users/login", methods=["POST"])
def login_user():
    data = request.json
    user = users_collection.find_one({"email": data["email"]})
    if user and check_password_hash(user["password"], data["password"]):
        return jsonify({"message": "Login successful", "user_id": str(user["_id"])}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        product_id = ObjectId(product_id)
    except Exception as e:
        return jsonify({"message": "Invalid product ID format"}), 400

    result = products_collection.delete_one({"_id": product_id})

    if result.deleted_count > 0:
        return jsonify({"message": "Product deleted successfully"}), 200
    else:
        return jsonify({"message": "Product not found"}), 404


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.json
    order = {
        "user_id": ObjectId(data["user_id"]),
        "product_ids": [ObjectId(pid) for pid in data["product_ids"]],
        "status": "pending",
        "timestamp": datetime.utcnow(),
    }
    order_id = orders_collection.insert_one(order).inserted_id
    return jsonify({"message": "Order created", "order_id": str(order_id)}), 201

@app.route("/orders/<user_id>", methods=["GET"])
def get_user_orders(user_id):
    orders = list(orders_collection.find({"user_id": ObjectId(user_id)}))
    for order in orders:
        order["_id"] = str(order["_id"])
        order["user_id"] = str(order["user_id"])
        order["product_ids"] = [str(pid) for pid in order["product_ids"]]
    return jsonify(orders), 200

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

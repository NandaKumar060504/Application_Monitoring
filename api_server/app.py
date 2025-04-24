from flask import Flask, request, jsonify
import time
import json
import uuid
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Simulated database
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
    {"id": 3, "name": "Bob Johnson", "email": "bob@example.com"},
]

products = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Phone", "price": 699.99},
    {"id": 3, "name": "Tablet", "price": 299.99},
    {"id": 4, "name": "Headphones", "price": 149.99},
]

orders = []

def log_request(endpoint, status_code, response_time):
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "request_id": str(uuid.uuid4()),
        "endpoint": endpoint,
        "status_code": status_code,
        "response_time_ms": response_time,
        "host": request.host,
        "method": request.method,
        "path": request.path,
        "user_agent": request.headers.get('User-Agent', 'Unknown'),
        "remote_addr": request.remote_addr
    }
    print(json.dumps(log_data))
    return log_data

@app.route('/health', methods=['GET'])
def health_check():
    start_time = time.time()
    time.sleep(0.03)  # fixed short delay
    response_time = (time.time() - start_time) * 1000
    log_request("/health", 200, response_time)
    return jsonify({"status": "healthy"}), 200

@app.route('/users', methods=['GET'])
def get_users():
    start_time = time.time()
    time.sleep(0.1)
    response_time = (time.time() - start_time) * 1000
    log_request("/users", 200, response_time)
    return jsonify(users), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    start_time = time.time()
    time.sleep(0.05)
    response_time = (time.time() - start_time) * 1000
    user = next((u for u in users if u["id"] == user_id), None)
    status_code = 200 if user else 404
    log_request(f"/users/{user_id}", status_code, response_time)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/products', methods=['GET'])
def get_products():
    start_time = time.time()
    time.sleep(0.1)
    response_time = (time.time() - start_time) * 1000
    log_request("/products", 200, response_time)
    return jsonify(products), 200

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    start_time = time.time()
    time.sleep(0.05)
    response_time = (time.time() - start_time) * 1000
    product = next((p for p in products if p["id"] == product_id), None)
    status_code = 200 if product else 404
    log_request(f"/products/{product_id}", status_code, response_time)
    if product:
        return jsonify(product), 200
    else:
        return jsonify({"error": "Product not found"}), 404

@app.route('/orders', methods=['GET'])
def get_orders():
    start_time = time.time()
    time.sleep(0.15)
    response_time = (time.time() - start_time) * 1000
    log_request("/orders", 200, response_time)
    return jsonify(orders), 200

@app.route('/orders', methods=['POST'])
def create_order():
    start_time = time.time()
    time.sleep(0.2)
    response_time = (time.time() - start_time) * 1000
    try:
        new_order = request.json
        new_order["id"] = len(orders) + 1
        new_order["timestamp"] = datetime.now().isoformat()
        orders.append(new_order)
        log_request("/orders (POST)", 201, response_time)
        return jsonify(new_order), 201
    except Exception as e:
        log_request("/orders (POST)", 400, response_time)
        return jsonify({"error": str(e)}), 400

@app.route('/search', methods=['GET'])
def search():
    start_time = time.time()
    time.sleep(0.4)
    response_time = (time.time() - start_time) * 1000
    query = request.args.get('q', '')
    results = [p for p in products if query.lower() in p["name"].lower()]
    log_request("/search", 200, response_time)
    return jsonify({"query": query, "results": results}), 200

@app.route('/login', methods=['POST'])
def login():
    start_time = time.time()
    time.sleep(0.2)
    response_time = (time.time() - start_time) * 1000
    log_request("/login", 200, response_time)
    return jsonify({"success": True, "token": "simulated_token_123"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

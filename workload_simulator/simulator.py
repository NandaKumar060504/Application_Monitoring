# workload_simulator/simulator.py
import requests
import random
import time
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
API_BASE_URL = "http://api_server:5000"  # Docker service name
REQUEST_RATE = 5  # Requests per second
ENDPOINTS = [
    {"path": "/health", "method": "GET", "weight": 10},
    {"path": "/users", "method": "GET", "weight": 15},
    {"path": "/users/1", "method": "GET", "weight": 5},
    {"path": "/users/2", "method": "GET", "weight": 5},
    {"path": "/users/3", "method": "GET", "weight": 5},
    {"path": "/users/4", "method": "GET", "weight": 2},  # This will cause 404
    {"path": "/products", "method": "GET", "weight": 20},
    {"path": "/products/1", "method": "GET", "weight": 8},
    {"path": "/products/2", "method": "GET", "weight": 8},
    {"path": "/products/3", "method": "GET", "weight": 8},
    {"path": "/products/4", "method": "GET", "weight": 8},
    {"path": "/products/5", "method": "GET", "weight": 2},  # This will cause 404
    {"path": "/orders", "method": "GET", "weight": 10},
    {"path": "/orders", "method": "POST", "weight": 5, "data": lambda: {"user_id": random.randint(1, 3), "product_id": random.randint(1, 4), "quantity": random.randint(1, 5)}},
    {"path": "/search", "method": "GET", "weight": 15, "params": lambda: {"q": random.choice(["laptop", "phone", "tablet", "headphones", "keyboard", "mouse", ""])}},
    {"path": "/login", "method": "POST", "weight": 10, "data": lambda: {"username": "test_user", "password": "password"}}
]

def select_endpoint():
    """Select a random endpoint based on weights"""
    total_weight = sum(endpoint["weight"] for endpoint in ENDPOINTS)
    r = random.uniform(0, total_weight)
    upto = 0
    for endpoint in ENDPOINTS:
        upto += endpoint["weight"]
        if upto >= r:
            return endpoint
    return ENDPOINTS[-1]  # Fallback

def simulate_traffic():
    """Generate traffic to API endpoints"""
    while True:
        endpoint = select_endpoint()
        url = f"{API_BASE_URL}{endpoint['path']}"
        method = endpoint["method"]
        
        kwargs = {}
        if "params" in endpoint:
            kwargs["params"] = endpoint["params"]() if callable(endpoint["params"]) else endpoint["params"]
        if "data" in endpoint:
            data = endpoint["data"]() if callable(endpoint["data"]) else endpoint["data"]
            kwargs["json"] = data
        
        try:
            logger.info(f"Sending {method} request to {url}")
            start_time = time.time()
            if method == "GET":
                response = requests.get(url, **kwargs)
            elif method == "POST":
                response = requests.post(url, **kwargs)
            else:
                logger.warning(f"Unsupported method: {method}")
                continue
            
            elapsed = (time.time() - start_time) * 1000  # ms
            logger.info(f"Response: {response.status_code} in {elapsed:.2f}ms")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
        
        # Sleep between requests (with some randomness)
        time.sleep(1.0 / REQUEST_RATE * random.uniform(0.8, 1.2))

if __name__ == "__main__":
    # Wait for API server to be ready
    logger.info("Waiting for API server to start...")
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            requests.get(f"{API_BASE_URL}/health", timeout=1)
            logger.info("API server is ready. Starting workload simulation.")
            break
        except requests.exceptions.RequestException:
            retry_count += 1
            logger.info(f"API server not ready. Retrying ({retry_count}/{max_retries})...")
            time.sleep(2)
    
    if retry_count >= max_retries:
        logger.error("Failed to connect to API server. Exiting.")
        exit(1)
    
    # Start simulating traffic
    simulate_traffic()
import requests

def test_api_endpoints():
    print("=== Testing API Endpoints ===")
    
    base_url = "http://localhost:5000"
    
    # Test 1: Health check
    print("\n1. Testing health check:")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Test route
    print("\n2. Testing test route:")
    try:
        response = requests.get(f"{base_url}/api/test")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Get products
    print("\n3. Testing get products:")
    try:
        response = requests.get(f"{base_url}/api/products")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Number of products: {len(response.json())}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Update product status (without authentication)
    print("\n4. Testing update product status:")
    try:
        # Use a valid product ID
        product_id = "69830ca91c2d724587bbbb04"
        response = requests.put(
            f"{base_url}/api/products/{product_id}/status",
            json={"status": "approved"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_api_endpoints()

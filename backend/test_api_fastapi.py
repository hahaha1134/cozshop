from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_api_endpoints():
    print("=== Testing API Endpoints ===")
    
    # Test 1: Health check
    print("\n1. Testing health check:")
    response = client.get("/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test 2: Test route
    print("\n2. Testing test route:")
    response = client.get("/api/test")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test 3: Get products
    print("\n3. Testing get products:")
    response = client.get("/api/products")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Number of products: {len(response.json())}")
    else:
        print(f"   Error: {response.text}")
    
    # Test 4: Update product status
    print("\n4. Testing update product status:")
    # Use a valid product ID
    product_id = "69830ca91c2d724587bbbb04"
    response = client.put(
        f"/api/products/{product_id}/status",
        json={"status": "approved"}
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text}")

if __name__ == "__main__":
    test_api_endpoints()

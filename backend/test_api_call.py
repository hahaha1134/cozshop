import httpx
import asyncio

async def test_api_call():
    print("=== Testing API Call ===")
    
    try:
        # Make a direct API call to get products
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:5000/api/products")
            
            print(f"\nAPI Response Status: {response.status_code}")
            
            if response.status_code == 200:
                products = response.json()
                print(f"Number of products returned by API: {len(products)}")
                
                if products:
                    print("\nFirst 3 products returned:")
                    for product in products[:3]:
                        print(f"- {product.get('name')} (ID: {product.get('id')})")
                else:
                    print("No products returned by API")
            else:
                print(f"API Error: {response.text}")
                
    except Exception as e:
        print(f"Error making API call: {e}")

if __name__ == '__main__':
    asyncio.run(test_api_call())

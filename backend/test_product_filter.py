from database import get_database
import asyncio

async def test_product_filter():
    db = get_database()
    
    print("=== Testing Product Filter Logic ===")
    
    # Test 1: Get all products
    all_products = await db.products.find().to_list(length=20)
    print(f"\n1. Total products in database: {len(all_products)}")
    
    # Test 2: Get products that should be visible (approved or no status)
    visible_query = {
        "$or": [
            {"status": "approved"},
            {"status": {"$exists": False}}
        ]
    }
    visible_products = await db.products.find(visible_query).to_list(length=20)
    print(f"2. Products that should be visible: {len(visible_products)}")
    
    # Test 3: Get inactive products
    inactive_products = await db.products.find({"status": "inactive"}).to_list(length=20)
    print(f"3. Inactive products: {len(inactive_products)}")
    
    # Test 4: Show details of inactive products
    if inactive_products:
        print("\n4. Details of inactive products:")
        for product in inactive_products:
            print(f"   - {product.get('name')} (ID: {product.get('_id')})")
            print(f"     Status: {product.get('status')}")
    
    # Test 5: Show details of visible products
    if visible_products:
        print("\n5. Details of visible products:")
        for product in visible_products[:3]:  # Show first 3
            print(f"   - {product.get('name')} (ID: {product.get('_id')})")
            print(f"     Status: {product.get('status')}")
    
    # Close connection
    await db.client.close()

if __name__ == '__main__':
    asyncio.run(test_product_filter())

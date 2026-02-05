import asyncio
from database import get_database
from bson import ObjectId

async def check_product_status():
    print("=== Checking Product Status in Database ===")
    db = get_database()
    
    # Get all products with status
    products = await db.products.find({}).to_list(length=100)
    print(f"Found {len(products)} products in database:")
    
    for i, product in enumerate(products):
        print(f"\nProduct {i+1}:")
        print(f"  ID: {product.get('_id')}")
        print(f"  Name: {product.get('name')}")
        print(f"  Status: {product.get('status', 'NOT SET')}")
        print(f"  Created at: {product.get('created_at')}")

if __name__ == "__main__":
    asyncio.run(check_product_status())

from database import get_database
import asyncio

async def check_product_status():
    db = get_database()
    
    # Get sample products to check their structure
    products = await db.products.find().limit(3).to_list(length=3)
    print(f"Found {len(products)} products")
    
    for i, product in enumerate(products):
        print(f"\nProduct {i+1}:")
        print(f"  ID: {product.get('_id')}")
        print(f"  Name: {product.get('name')}")
        print(f"  Status: {product.get('status')}")
        print(f"  All fields: {list(product.keys())}")
    
    # Check if any products have status field
    status_products = await db.products.count_documents({"status": {"$exists": True}})
    print(f"\nProducts with status field: {status_products}")
    
    # Check distinct status values
    if status_products > 0:
        status_values = await db.products.distinct("status")
        print(f"Status values: {status_values}")
    
    # Close connection
    await db.client.close()

if __name__ == '__main__':
    asyncio.run(check_product_status())

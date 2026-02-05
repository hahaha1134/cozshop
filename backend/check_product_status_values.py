from database import get_database
import asyncio

async def check_product_status_values():
    db = get_database()
    
    # Get all distinct status values
    status_values = await db.products.distinct("status")
    print(f"All status values: {status_values}")
    
    # Count products by status
    for status in status_values:
        count = await db.products.count_documents({"status": status})
        print(f"Products with status '{status}': {count}")
    
    # Count products without status
    no_status_count = await db.products.count_documents({"status": {"$exists": False}})
    print(f"Products without status: {no_status_count}")
    
    # Get total products
    total_count = await db.products.count_documents({})
    print(f"Total products: {total_count}")
    
    # Close connection
    await db.client.close()

if __name__ == '__main__':
    asyncio.run(check_product_status_values())

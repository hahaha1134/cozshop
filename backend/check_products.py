from database import get_database
import asyncio

async def check_products():
    db = get_database()
    products = await db.products.find().to_list(length=100)
    print(f"Total products: {len(products)}")
    for product in products:
        print(f"Product: {product['name']}, Stock: {product.get('stock', 'N/A')}, Status: {product.get('status', 'N/A')}")

if __name__ == "__main__":
    asyncio.run(check_products())

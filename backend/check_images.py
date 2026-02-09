from database import get_database
import asyncio

async def check_products():
    db = get_database()
    products = await db.products.find().to_list(length=10)
    for p in products:
        print(f'Product: {p.get("name")}, Image: {p.get("image")}')

if __name__ == "__main__":
    asyncio.run(check_products())

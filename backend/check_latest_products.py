from database import get_database
import asyncio

async def check_latest_products():
    db = get_database()
    products = await db.products.find().sort('created_at', -1).to_list(length=5)
    for p in products:
        print(f'Product: {p.get("name")}, Created: {p.get("created_at")}, Image: {p.get("image")}')

if __name__ == "__main__":
    asyncio.run(check_latest_products())

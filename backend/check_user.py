from database import get_database
import asyncio

async def main():
    db = get_database()
    user = await db.users.find_one({})
    print(user)
    await db.client.close()

asyncio.run(main())

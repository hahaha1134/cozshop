from database import get_database
import asyncio

async def check_users():
    db = get_database()
    users = await db.users.find().to_list(length=100)
    print(f"Total users: {len(users)}")
    for user in users:
        print(f"User: {user['name']}, Email: {user['email']}, Status: {user.get('status', 'active')}")

if __name__ == "__main__":
    asyncio.run(check_users())

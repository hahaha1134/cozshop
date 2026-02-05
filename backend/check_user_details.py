from database import get_database
import asyncio

async def check_user_details():
    db = get_database()
    users = await db.users.find().to_list(length=100)
    print(f"Total users: {len(users)}")
    for user in users:
        print(f"User: {user['name']}, Email: {user['email']}, Status: {user.get('status', 'active')}, Role: {user.get('role', 'user')}")
        print(f"Password: {user.get('password', 'No password found')}")
        print("---")

if __name__ == "__main__":
    asyncio.run(check_user_details())

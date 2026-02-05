import asyncio
from database import get_database

async def check_user_details():
    print("=== Checking User Details in Database ===")
    db = get_database()
    
    # Get all users with password
    users = await db.users.find({}).to_list(length=100)
    print(f"Found {len(users)} users in database:")
    
    for i, user in enumerate(users):
        print(f"\nUser {i+1}:")
        print(f"  ID: {user.get('_id')}")
        print(f"  Name: {user.get('name')}")
        print(f"  Email: {user.get('email')}")
        print(f"  Password: {user.get('password')}")
        print(f"  Role: {user.get('role')}")
        print(f"  Created at: {user.get('created_at')}")
    
    # Check if any admin user exists
    admin_users = await db.users.find({"role": "admin"}).to_list(length=100)
    print(f"\n=== Admin Users ===")
    print(f"Found {len(admin_users)} admin users:")
    
    for i, user in enumerate(admin_users):
        print(f"\nAdmin {i+1}:")
        print(f"  ID: {user.get('_id')}")
        print(f"  Name: {user.get('name')}")
        print(f"  Email: {user.get('email')}")
        print(f"  Password: {user.get('password')}")

if __name__ == "__main__":
    asyncio.run(check_user_details())

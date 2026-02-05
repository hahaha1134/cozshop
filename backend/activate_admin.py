from database import get_database
import asyncio
from bson import ObjectId

async def activate_admin():
    db = get_database()
    
    # Find admin user by email
    admin_user = await db.users.find_one({"email": "admin@cozshop.com"})
    
    if not admin_user:
        print("Admin user not found!")
        return
    
    # Update user status to active
    result = await db.users.update_one(
        {"_id": admin_user["_id"]},
        {"$set": {"status": "active"}}
    )
    
    if result.modified_count > 0:
        print("✓ Admin user activated successfully!")
        print(f"Admin user: {admin_user['name']} ({admin_user['email']})")
        print("Status: active")
        print("Password: admin123")
    else:
        print("Admin user is already active!")

if __name__ == "__main__":
    asyncio.run(activate_admin())

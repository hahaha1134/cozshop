from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

client = AsyncIOMotorClient(settings.MONGODB_URI)
database = client.cozshop

def get_database():
    return database

async def connect_to_mongo():
    """Connect to MongoDB"""
    try:
        await client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

async def close_mongo_connection():
    """Close MongoDB connection"""
    client.close()
    print("Closed MongoDB connection")
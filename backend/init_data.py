import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from datetime import datetime
from auth import get_password_hash

async def init_data():
    # Connect to MongoDB
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client.cozshop
    
    # Clear existing data
    await db.users.delete_many({})
    await db.products.delete_many({})
    
    # Create admin user
    admin_user = {
        "name": "Admin User",
        "email": "admin@cozshop.com",
        "password": get_password_hash("admin123"),
        "role": "admin",
        "created_at": datetime.utcnow()
    }
    await db.users.insert_one(admin_user)
    print("✓ Admin user created (email: admin@cozshop.com, password: admin123)")
    
    # Create sample products
    products = [
        {
            "name": "Wireless Headphones",
            "description": "Premium wireless headphones with noise cancellation and 30-hour battery life. Perfect for music lovers and professionals.",
            "price": 199.99,
            "category": "Electronics",
            "stock": 50,
            "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400",
            "rating": 4.5,
            "numReviews": 128,
            "created_at": datetime.utcnow()
        },
        {
            "name": "Smart Watch Pro",
            "description": "Advanced smartwatch with health monitoring, GPS, and 7-day battery life. Water-resistant up to 50 meters.",
            "price": 299.99,
            "category": "Electronics",
            "stock": 35,
            "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400",
            "rating": 4.7,
            "numReviews": 256,
            "created_at": datetime.utcnow()
        },
        {
            "name": "Laptop Backpack",
            "description": "Durable and stylish backpack with padded laptop compartment, USB charging port, and multiple pockets.",
            "price": 79.99,
            "category": "Accessories",
            "stock": 100,
            "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400",
            "rating": 4.3,
            "numReviews": 89,
            "created_at": datetime.utcnow()
        },
        {
            "name": "Wireless Mouse",
            "description": "Ergonomic wireless mouse with precision tracking and long battery life. Works on any surface.",
            "price": 49.99,
            "category": "Electronics",
            "stock": 150,
            "image": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400",
            "rating": 4.2,
            "numReviews": 167,
            "created_at": datetime.utcnow()
        },
        {
            "name": "USB-C Hub",
            "description": "7-in-1 USB-C hub with HDMI, USB 3.0 ports, SD card reader, and power delivery. Perfect for laptops.",
            "price": 59.99,
            "category": "Accessories",
            "stock": 75,
            "image": "https://images.unsplash.com/photo-1625723044792-44de16ccb4e9?w=400",
            "rating": 4.4,
            "numReviews": 92,
            "created_at": datetime.utcnow()
        },
        {
            "name": "Mechanical Keyboard",
            "description": "RGB mechanical keyboard with Cherry MX switches, programmable keys, and aluminum frame.",
            "price": 149.99,
            "category": "Electronics",
            "stock": 40,
            "image": "https://images.unsplash.com/photo-1595225476474-87563907a212?w=400",
            "rating": 4.6,
            "numReviews": 203,
            "created_at": datetime.utcnow()
        },
        {
            "name": "Portable SSD 1TB",
            "description": "Ultra-fast portable SSD with 1TB storage. USB 3.2 Gen 2 for speeds up to 1050MB/s.",
            "price": 129.99,
            "category": "Electronics",
            "stock": 60,
            "image": "https://images.unsplash.com/photo-1531492746076-161ca9bcad58?w=400",
            "rating": 4.8,
            "numReviews": 145,
            "created_at": datetime.utcnow()
        },
        {
            "name": "Webcam HD 1080p",
            "description": "Full HD webcam with auto-focus, built-in microphone, and low-light correction. Great for video calls.",
            "price": 89.99,
            "category": "Electronics",
            "stock": 80,
            "image": "https://images.unsplash.com/photo-1587826080692-f439cd0b70da?w=400",
            "rating": 4.1,
            "numReviews": 78,
            "created_at": datetime.utcnow()
        },
        {
            "name": "Desk Lamp LED",
            "description": "Modern LED desk lamp with adjustable brightness, color temperature control, and USB charging port.",
            "price": 69.99,
            "category": "Accessories",
            "stock": 120,
            "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400",
            "rating": 4.5,
            "numReviews": 134,
            "created_at": datetime.utcnow()
        },
        {
            "name": "Phone Stand",
            "description": "Adjustable aluminum phone stand compatible with all smartphones and tablets. Non-slip base.",
            "price": 29.99,
            "category": "Accessories",
            "stock": 200,
            "image": "https://images.unsplash.com/photo-1586816879360-004f5b0c51e5?w=400",
            "rating": 4.3,
            "numReviews": 167,
            "created_at": datetime.utcnow()
        },
        {
            "name": "Bluetooth Speaker",
            "description": "Portable Bluetooth speaker with 360° sound, waterproof design, and 20-hour battery life.",
            "price": 119.99,
            "category": "Electronics",
            "stock": 55,
            "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400",
            "rating": 4.6,
            "numReviews": 289,
            "created_at": datetime.utcnow()
        },
        {
            "name": "Cable Organizer",
            "description": "Set of cable organizers and ties to keep your workspace neat and tidy. Multiple sizes included.",
            "price": 19.99,
            "category": "Accessories",
            "stock": 300,
            "image": "https://images.unsplash.com/photo-1558346490-a72e53ae2d4f?w=400",
            "rating": 4.0,
            "numReviews": 95,
            "created_at": datetime.utcnow()
        }
    ]
    
    await db.products.insert_many(products)
    print(f"✓ {len(products)} sample products created")
    
    print("\n✅ Database initialization completed successfully!")
    print("\nYou can now:")
    print("  - Login as admin: admin@cozshop.com / admin123")
    print("  - Register new users")
    print("  - Browse and purchase products")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(init_data())
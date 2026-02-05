from database import get_database
import asyncio
from datetime import datetime, timedelta
from bson import ObjectId

async def init_test_orders():
    db = get_database()
    
    # Check if there are already orders
    existing_orders = await db.orders.count_documents({})
    if existing_orders > 0:
        print(f'已有 {existing_orders} 个订单，跳过初始化')
        return
    
    # Get some products
    products = await db.products.find().limit(5).to_list(length=5)
    if len(products) == 0:
        print('没有商品数据，无法创建订单')
        return
    
    # Create test orders
    test_orders = []
    

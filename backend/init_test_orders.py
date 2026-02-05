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
    
    # Create orders for the last 6 months
    for i in range(6):
        # Create 2-3 orders per month
        for j in range(2 + i % 2):
            # Random products for this order
            order_products = products[:2 + j % 2]
            items = []
            total_price = 0
            
            for product in order_products:
                quantity = 1 + j % 2
                item_price = product.get('price', 0)
                items.append({
                    'product_id': product.get('_id'),
                    'name': product.get('name'),
                    'price': item_price,
                    'quantity': quantity,
                    'image': product.get('image')
                })
                total_price += item_price * quantity
            
            # Create order date (i months ago)
            order_date = datetime.utcnow() - timedelta(days=i*30 + j*10)
            
            # Random status
            statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
            status = statuses[(i + j) % len(statuses)]
            
            order = {
                'user_id': ObjectId('60d0fe4f5311236168a109ca'),  # Test user ID
                'items': items,
                'total_price': round(total_price, 2),
                'status': status,
                'shipping_address': {
                    'name': 'Test User',
                    'phone': '
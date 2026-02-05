from database import get_database
import asyncio

async def check_orders():
    db = get_database()
    
    # Check orders count
    orders_count = await db.orders.count_documents({})
    print(f'Total orders: {orders_count}')
    
    # Check if there are any orders
    if orders_count > 0:
        # Get some orders
        orders = await db.orders.find().limit(5).to_list(length=5)
        print('\nFirst 5 orders:')
        for i, order in enumerate(orders):
            print(f'Order {i+1}:')
            print(f'  ID: {order.get("_id")}')
            print(f'  Status: {order.get("status")}')
            print(f'  Total price: {order.get("total_price")}')
            print(f'  Created at: {order.get("created_at")}')
            print(f'  Items: {len(order.get("items", []))} items')
            print()
    else:
        print('\nNo orders found in database')
    
    # Check products
    products_count = await db.products.count_documents({})
    print(f'Total products: {products_count}')
    
    # Close connection
    await db.client.close()

if __name__ == '__main__':
    asyncio.run(check_orders())

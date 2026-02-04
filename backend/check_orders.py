from database import get_database
import asyncio

async def main():
    db = get_database()
    # 检查所有订单
    orders = await db.orders.find().to_list(length=100)
    print('Orders found:', len(orders))
    
    for order in orders:
        print('\nOrder ID:', str(order.get('_id')))
        print('User ID:', order.get('user_id'))
        print('Status:', order.get('status'))
        print('Order Items:', order.get('orderItems', []))
        print('Total Price:', order.get('totalPrice'))
    
    # 检查用户
    users = await db.users.find().to_list(length=100)
    print('\n\nUsers found:', len(users))
    for user in users:
        print('User ID:', str(user.get('_id')))
        print('User Role:', user.get('role'))

if __name__ == '__main__':
    asyncio.run(main())
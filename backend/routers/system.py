from fastapi import APIRouter, Depends
from auth import get_current_admin
from database import get_database
from datetime import datetime, timedelta
from bson import ObjectId

router = APIRouter(prefix="/api/system", tags=["System"])

@router.get("/status")
async def get_system_status(admin_id: str = Depends(get_current_admin)):
    db = get_database()
    
    # Get total users
    total_users = await db.users.count_documents({})
    
    # Get total products
    total_products = await db.products.count_documents({})
    
    # Get total orders
    total_orders = await db.orders.count_documents({})
    
    # Get total revenue (sum of all order total prices)
    orders = await db.orders.find().to_list(length=1000)
    total_revenue = sum(order.get("total_price", 0) for order in orders)
    
    # Get recent orders (last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_orders = await db.orders.count_documents({"created_at": {"$gte": seven_days_ago}})
    
    # Get order status counts
    status_counts = {
        "pending": await db.orders.count_documents({"status": "pending"}),
        "processing": await db.orders.count_documents({"status": "processing"}),
        "shipped": await db.orders.count_documents({"status": "shipped"}),
        "delivered": await db.orders.count_documents({"status": "delivered"}),
        "cancelled": await db.orders.count_documents({"status": "cancelled"})
    }
    
    return {
        "status": "operational",
        "timestamp": datetime.utcnow(),
        "statistics": {
            "total_users": total_users,
            "total_products": total_products,
            "total_orders": total_orders,
            "total_revenue": round(total_revenue, 2),
            "recent_orders": recent_orders,
            "order_statuses": status_counts
        }
    }

@router.get("/stats")
async def get_system_statistics(admin_id: str = Depends(get_current_admin)):
    db = get_database()
    
    # Get monthly sales data for the last 6 months
    sales_data = []
    now = datetime.utcnow()
    
    for i in range(6):
        month_start = (now - timedelta(days=i*30)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_end = (month_start + timedelta(days=30)).replace(hour=23, minute=59, second=59, microsecond=999999)
        
        month_orders = await db.orders.find({
            "created_at": {"$gte": month_start, "$lte": month_end}
        }).to_list(length=1000)
        
        month_revenue = sum(order.get("total_price", 0) for order in month_orders)
        
        sales_data.append({
            "month": month_start.strftime("%Y-%m"),
            "orders": len(month_orders),
            "revenue": round(month_revenue, 2)
        })
    
    # Get top selling products
    product_sales = {}
    all_orders = await db.orders.find().to_list(length=1000)
    
    for order in all_orders:
        for item in order.get("items", []):
            product_id = item.get("product_id")
            if product_id:
                if product_id not in product_sales:
                    product_sales[product_id] = {
                        "quantity": 0,
                        "revenue": 0
                    }
                product_sales[product_id]["quantity"] += item.get("quantity", 0)
                product_sales[product_id]["revenue"] += item.get("price", 0) * item.get("quantity", 0)
    
    # Convert to list and sort
    top_products = []
    for product_id, sales in product_sales.items():
        # Get product details
        product = await db.products.find_one({"_id": product_id})
        if product:
            top_products.append({
                "id": product_id,
                "name": product.get("name"),
                "category": product.get("category"),
                "quantity_sold": sales["quantity"],
                "revenue": round(sales["revenue"], 2)
            })
    
    # Sort by quantity sold
    top_products.sort(key=lambda x: x["quantity_sold"], reverse=True)
    top_products = top_products[:10]  # Top 10
    
    return {
        "monthly_sales": sales_data,
        "top_products": top_products
    }

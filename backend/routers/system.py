from fastapi import APIRouter, Depends, Body
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

@router.get("/today")
async def get_today_stats(admin_id: str = Depends(get_current_admin)):
    db = get_database()
    
    # Get today's date (start and end)
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999999)
    
    # Get today's new products
    today_products = await db.products.count_documents({
        "created_at": {"$gte": today_start, "$lte": today_end}
    })
    
    # Get today's new orders
    today_orders = await db.orders.count_documents({
        "created_at": {"$gte": today_start, "$lte": today_end}
    })
    
    # Get today's new users
    today_users = await db.users.count_documents({
        "created_at": {"$gte": today_start, "$lte": today_end}
    })
    
    return {
        "today": {
            "products": today_products,
            "orders": today_orders,
            "users": today_users
        }
    }

@router.get("/announcements")
async def get_announcements(admin_id: str = Depends(get_current_admin)):
    db = get_database()
    announcements = await db.announcements.find().sort("created_at", -1).to_list(length=100)
    
    # Convert to response format
    result = []
    for announcement in announcements:
        result.append({
            "id": str(announcement["_id"]),
            "title": announcement["title"],
            "content": announcement["content"],
            "created_at": announcement["created_at"]
        })
    
    return result

@router.post("/announcements")
async def create_announcement(title: str = Body(..., description="公告标题"), content: str = Body(..., description="公告内容"), admin_id: str = Depends(get_current_admin)):
    db = get_database()
    
    announcement = {
        "title": title,
        "content": content,
        "created_at": datetime.utcnow()
    }
    
    result = await db.announcements.insert_one(announcement)
    
    return {
        "id": str(result.inserted_id),
        "title": title,
        "content": content,
        "created_at": announcement["created_at"]
    }

@router.put("/announcements/{announcement_id}")
async def update_announcement(announcement_id: str, title: str = Body(..., description="公告标题"), content: str = Body(..., description="公告内容"), admin_id: str = Depends(get_current_admin)):
    db = get_database()
    
    result = await db.announcements.update_one(
        {"_id": ObjectId(announcement_id)},
        {"$set": {"title": title, "content": content}}
    )
    
    if result.modified_count == 0:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Announcement not found"
        )
    
    return {"message": "Announcement updated successfully"}

@router.delete("/announcements/{announcement_id}")
async def delete_announcement(announcement_id: str, admin_id: str = Depends(get_current_admin)):
    db = get_database()
    
    result = await db.announcements.delete_one({"_id": ObjectId(announcement_id)})
    
    if result.deleted_count == 0:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Announcement not found"
        )
    
    return {"message": "Announcement deleted successfully"}

@router.post("/cleanup")
async def cleanup_invalid_data(admin_id: str = Depends(get_current_admin)):
    db = get_database()
    
    # Cleanup incomplete orders (older than 24 hours)
    twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
    incomplete_orders = await db.orders.delete_many(
        {"status": "pending", "created_at": {"$lt": twenty_four_hours_ago}}
    )
    
    # Cleanup invalid user accounts (no email or name)
    invalid_users = await db.users.delete_many(
        {"$or": [{"email": {"$exists": False}}, {"name": {"$exists": False}}]}
    )
    
    # Cleanup products with no name or price
    invalid_products = await db.products.delete_many(
        {"$or": [{"name": {"$exists": False}}, {"price": {"$exists": False}}]}
    )
    
    return {
        "message": "Data cleanup completed",
        "cleaned": {
            "incomplete_orders": incomplete_orders.deleted_count,
            "invalid_users": invalid_users.deleted_count,
            "invalid_products": invalid_products.deleted_count
        }
    }

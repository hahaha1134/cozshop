from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models import OrderCreate, OrderResponse, OrderItem
from database import get_database
from auth import get_current_user, get_current_admin
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/api/orders", tags=["Orders"])

@router.get("", response_model=List[OrderResponse])
async def get_orders(user_id: str = Depends(get_current_user)):
    db = get_database()
    orders = await db.orders.find({"user_id": user_id}).to_list(length=100)
    orders.sort(key=lambda x: x["created_at"], reverse=True)
    
    return [
        OrderResponse(
            id=str(order["_id"]),
            user_id=order["user_id"],
            items=[
                OrderItem(
                    product_id=item["product_id"],
                    name=item["name"],
                    price=item["price"],
                    quantity=item["quantity"],
                    image=item.get("image", "https://via.placeholder.com/300x300")
                )
                for item in order["items"]
            ],
            total_price=order["total_price"],
            status=order["status"],
            shipping_address=order["shipping_address"],
            payment_method=order["payment_method"],
            created_at=order["created_at"]
        )
        for order in orders
    ]

@router.get("/all", response_model=List[OrderResponse])
async def get_all_orders(user_id: str = Depends(get_current_admin)):
    db = get_database()
    orders = await db.orders.find().to_list(length=100)
    orders.sort(key=lambda x: x["created_at"], reverse=True)
    
    return [
        OrderResponse(
            id=str(order["_id"]),
            user_id=order["user_id"],
            items=[
                OrderItem(
                    product_id=item["product_id"],
                    name=item["name"],
                    price=item["price"],
                    quantity=item["quantity"],
                    image=item.get("image", "https://via.placeholder.com/300x300")
                )
                for item in order["items"]
            ],
            total_price=order["total_price"],
            status=order["status"],
            shipping_address=order["shipping_address"],
            payment_method=order["payment_method"],
            created_at=order["created_at"]
        )
        for order in orders
    ]

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str, user_id: str = Depends(get_current_user)):
    db = get_database()
    try:
        order = await db.orders.find_one({"_id": ObjectId(order_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check if user owns the order or is admin
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if order["user_id"] != user_id and user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this order"
        )
    
    return OrderResponse(
        id=str(order["_id"]),
        user_id=order["user_id"],
        items=[
            OrderItem(
                product_id=item["product_id"],
                name=item["name"],
                price=item["price"],
                quantity=item["quantity"],
                image=item.get("image", "https://via.placeholder.com/300x300")
            )
            for item in order["items"]
        ],
        total_price=order["total_price"],
        status=order["status"],
        shipping_address=order["shipping_address"],
        payment_method=order["payment_method"],
        created_at=order["created_at"]
    )

@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate, user_id: str = Depends(get_current_user)):
    db = get_database()
    
    # Get cart
    cart = await db.carts.find_one({"user_id": user_id})
    if not cart or not cart["items"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )
    
    # Calculate total price
    total_price = sum(item["price"] * item["quantity"] for item in cart["items"])
    
    # Create order
    order_dict = {
        "user_id": user_id,
        "items": cart["items"],
        "total_price": total_price,
        "status": "pending",
        "shipping_address": order_data.shipping_address,
        "payment_method": order_data.payment_method,
        "created_at": datetime.utcnow()
    }
    
    result = await db.orders.insert_one(order_dict)
    created_order = await db.orders.find_one({"_id": result.inserted_id})
    
    # Clear cart
    await db.carts.delete_one({"user_id": user_id})
    
    # Update product stock
    for item in cart["items"]:
        await db.products.update_one(
            {"_id": ObjectId(item["product_id"])},
            {"$inc": {"stock": -item["quantity"]}}
        )
    
    return OrderResponse(
        id=str(created_order["_id"]),
        user_id=created_order["user_id"],
        items=[
            OrderItem(
                product_id=item["product_id"],
                name=item["name"],
                price=item["price"],
                quantity=item["quantity"],
                image=item.get("image", "https://via.placeholder.com/300x300")
            )
            for item in created_order["items"]
        ],
        total_price=created_order["total_price"],
        status=created_order["status"],
        shipping_address=created_order["shipping_address"],
        payment_method=created_order["payment_method"],
        created_at=created_order["created_at"]
    )

@router.put("/{order_id}/status")
async def update_order_status(order_id: str, status: str, user_id: str = Depends(get_current_admin)):
    db = get_database()
    try:
        order = await db.orders.find_one({"_id": ObjectId(order_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    valid_statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    await db.orders.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": status}}
    )
    
    return {"message": "Order status updated successfully"}
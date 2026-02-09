from fastapi import APIRouter, Depends, HTTPException, status, Body
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
            orderNumber=order.get("order_number", ""),
            user_id=str(order["user_id"]),
            orderItems=[
                OrderItem(
                    product_id=str(item["product_id"]),
                    name=item["name"],
                    price=item["price"],
                    quantity=item["quantity"],
                    image=item.get("image", "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjZjBmMGMwIi8+CjxwYXRoIGQ9Ik0xNTAgMTUwIEMxNzcuNjEgMTUwIDE5NSAxMzIuNjEgMTk1IDEwNSBDMTk1IDc3LjM5IDE3Ny42MSA2MCAxNTAgNjAgQzEyMi4zOSA2MCAxMDUgNzcuMzkgMTA1IDEwNSBDMTA1IDEzMi42MSAxMjIuMzkgMTUwIDE1MCAxNTAiIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4yIi8+Cjx0ZXh0IHg9IjE1MCIgeT0iMTY1IiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiMwMDAiPk5vIEltYWdlPC90ZXh0Pgo8L3N2Zz4="))
                for item in order.get("items", [])
            ],
            totalPrice=order.get("total_price", 0),
            status=order["status"],
            shippingAddress=order.get("shipping_address", {}),
            paymentMethod=order.get("payment_method", ""),
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
            orderNumber=order.get("order_number", ""),
            user_id=str(order["user_id"]),
            orderItems=[
                OrderItem(
                    product_id=str(item["product_id"]),
                    name=item["name"],
                    price=item["price"],
                    quantity=item["quantity"],
                    image=item.get("image", "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjZjBmMGMwIi8+CjxwYXRoIGQ9Ik0xNTAgMTUwIEMxNzcuNjEgMTUwIDE5NSAxMzIuNjEgMTk1IDEwNSBDMTk1IDc3LjM5IDE3Ny42MSA2MCAxNTAgNjAgQzEyMi4zOSA2MCAxMDUgNzcuMzkgMTA1IDEwNSBDMTA1IDEzMi42MSAxMjIuMzkgMTUwIDE1MCAxNTAiIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4yIi8+Cjx0ZXh0IHg9IjE1MCIgeT0iMTY1IiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiMwMDAiPk5vIEltYWdlPC90ZXh0Pgo8L3N2Zz4="))
                for item in order.get("items", [])
            ],
            totalPrice=order.get("total_price", 0),
            status=order["status"],
            shippingAddress=order.get("shipping_address", {}),
            paymentMethod=order.get("payment_method", ""),
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
        orderNumber=order.get("order_number", ""),
        user_id=str(order["user_id"]),
        orderItems=[
            OrderItem(
                product_id=str(item["product_id"]),
                name=item["name"],
                price=item["price"],
                quantity=item["quantity"],
                image=item.get("image", "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjZjBmMGMwIi8+CjxwYXRoIGQ9Ik0xNTAgMTUwIEMxNzcuNjEgMTUwIDE5NSAxMzIuNjEgMTk1IDEwNSBDMTk1IDc3LjM5IDE3Ny42MSA2MCAxNTAgNjAgQzEyMi4zOSA2MCAxMDUgNzcuMzkgMTA1IDEwNSBDMTA1IDEzMi42MSAxMjIuMzkgMTUwIDE1MCAxNTAiIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4yIi8+Cjx0ZXh0IHg9IjE1MCIgeT0iMTY1IiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiMwMDAiPk5vIEltYWdlPC90ZXh0Pgo8L3N2Zz4="))
            for item in order.get("items", [])
        ],
        totalPrice=order.get("total_price", 0),
        status=order["status"],
        shippingAddress=order.get("shipping_address", {}),
        paymentMethod=order.get("payment_method", ""),
        created_at=order["created_at"]
    )

@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate, user_id: str = Depends(get_current_user)):
    db = get_database()
    
    # Get cart
    cart = await db.carts.find_one({"user_id": user_id})
    if not cart or not cart.get("items"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )
    
    # Calculate total price
    total_price = sum(item["price"] * item["quantity"] for item in cart["items"])
    
    # Generate order number: timestamp + user ID
    timestamp = int(datetime.utcnow().timestamp())
    order_number = f"{timestamp}{user_id[:8]}"
    
    # Create order
    order_dict = {
        "user_id": user_id,
        "order_number": order_number,
        "items": cart["items"],
        "total_price": total_price,
        "status": "pending",
        "shipping_address": order_data.shippingAddress.model_dump(),
        "payment_method": order_data.paymentMethod,
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
        orderNumber=created_order.get("order_number", ""),
        user_id=str(created_order["user_id"]),
        orderItems=[
            OrderItem(
                product_id=str(item["product_id"]),
                name=item["name"],
                price=item["price"],
                quantity=item["quantity"],
                image=item.get("image", "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjZjBmMGMwIi8+CjxwYXRoIGQ9Ik0xNTAgMTUwIEMxNzcuNjEgMTUwIDE5NSAxMzIuNjEgMTk1IDEwNSBDMTk1IDc3LjM5IDE3Ny42MSA2MCAxNTAgNjAgQzEyMi4zOSA2MCAxMDUgNzcuMzkgMTA1IDEwNSBDMTA1IDEzMi42MSAxMjIuMzkgMTUwIDE1MCAxNTAiIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4yIi8+Cjx0ZXh0IHg9IjE1MCIgeT0iMTY1IiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiMwMDAiPk5vIEltYWdlPC90ZXh0Pgo8L3N2Zz4="))
            for item in created_order.get("items", [])
        ],
        totalPrice=created_order.get("total_price", 0),
        status=created_order["status"],
        shippingAddress=created_order.get("shipping_address", {}),
        paymentMethod=created_order.get("payment_method", ""),
        created_at=created_order["created_at"]
    )

@router.put("/{order_id}/status")
async def update_order_status(order_id: str, status_data: dict = Body(...), user_id: str = Depends(get_current_admin)):
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
    
    status = status_data.get("status")
    if not status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status is required"
        )
    
    # 严格的状态流转逻辑
    current_status = order["status"]
    valid_transitions = {
        "pending": ["processing", "cancelled"],  # 待付款 -> 待发货或已取消
        "processing": ["shipped"],  # 待发货 -> 待收货
        "shipped": ["delivered"],  # 待收货 -> 已完成
        "delivered": [],  # 已完成 -> 无
        "cancelled": []  # 已取消 -> 无
    }
    
    if status not in valid_transitions.get(current_status, []):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status transition. From {current_status} you can only go to: {', '.join(valid_transitions.get(current_status, []))}"
        )
    
    await db.orders.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": status}}
    )
    
    return {"message": "Order status updated successfully"}

@router.put("/{order_id}/pay")
async def pay_order(order_id: str, user_id: str = Depends(get_current_user)):
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
    
    # Check if user owns the order
    if order["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this order"
        )
    
    # Check if order is in pending status
    if order["status"] != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order can only be paid if it's in pending status"
        )
    
    # Update status to processing (待发货)
    await db.orders.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": "processing", "paidAt": datetime.utcnow()}}
    )
    
    return {"message": "Order paid successfully"}

@router.put("/{order_id}/cancel")
async def cancel_order(order_id: str, user_id: str = Depends(get_current_user)):
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
    
    # Check if user owns the order
    if order["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this order"
        )
    
    # Check if order is in pending status
    if order["status"] != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order can only be cancelled if it's in pending status"
        )
    
    # Update status to cancelled
    await db.orders.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": "cancelled"}}
    )
    
    # Restore product stock
    for item in order.get("items", []):
        await db.products.update_one(
            {"_id": ObjectId(item["product_id"])},
            {"$inc": {"stock": item["quantity"]}}
        )
    
    return {"message": "Order cancelled successfully"}

@router.put("/{order_id}/deliver")
async def deliver_order(order_id: str, user_id: str = Depends(get_current_admin)):
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
    
    # Check if order is in processing status
    if order["status"] != "processing":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order can only be delivered if it's in processing status"
        )
    
    # Update status to shipped (待收货)
    await db.orders.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": "shipped"}}
    )
    
    return {"message": "Order delivered successfully"}

@router.put("/{order_id}/complete")
async def complete_order(order_id: str, user_id: str = Depends(get_current_user)):
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
    
    # Check if user owns the order
    if order["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this order"
        )
    
    # Check if order is in shipped status
    if order["status"] != "shipped":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order can only be completed if it's in shipped status"
        )
    
    # Update status to delivered (已完成)
    await db.orders.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": "delivered", "deliveredAt": datetime.utcnow()}}
    )
    
    return {"message": "Order completed successfully"}
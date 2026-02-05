from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models import CartItem, CartResponse
from database import get_database
from auth import get_current_user
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("", response_model=CartResponse)
async def get_cart(user_id: str = Depends(get_current_user)):
    db = get_database()
    cart = await db.carts.find_one({"user_id": user_id})
    
    if not cart:
        return CartResponse(user_id=user_id, items=[], total_items=0, total_price=0)
    
    total_items = sum(item["quantity"] for item in cart["items"])
    total_price = sum(item["price"] * item["quantity"] for item in cart["items"])
    
    return CartResponse(
        user_id=user_id,
        items=[
            CartItem(
                product_id=item["product_id"],
                name=item["name"],
                price=item["price"],
                quantity=item["quantity"],
                image=item.get("image", "https://via.placeholder.com/300x300")
            )
            for item in cart["items"]
        ],
        total_items=total_items,
        total_price=total_price
    )

@router.post("/items", response_model=CartResponse)
async def add_to_cart(item: CartItem, user_id: str = Depends(get_current_user)):
    db = get_database()
    cart = await db.carts.find_one({"user_id": user_id})
    
    if cart:
        # Check if product already exists in cart
        existing_item = next(
            (i for i in cart["items"] if i["product_id"] == item.product_id),
            None
        )
        if existing_item:
            # Update quantity
            await db.carts.update_one(
                {"user_id": user_id, "items.product_id": item.product_id},
                {"$inc": {"items.$.quantity": item.quantity}}
            )
        else:
            # Add new item
            await db.carts.update_one(
                {"user_id": user_id},
                {"$push": {"items": item.model_dump()}}
            )
    else:
        # Create new cart
        cart_data = {
            "user_id": user_id,
            "items": [item.model_dump()],
            "created_at": datetime.utcnow()
        }
        await db.carts.insert_one(cart_data)
    
    return await get_cart(user_id)

@router.put("/items/{product_id}", response_model=CartResponse)
async def update_cart_item(product_id: str, quantity: int, user_id: str = Depends(get_current_user)):
    db = get_database()
    cart = await db.carts.find_one({"user_id": user_id})
    
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )
    
    if quantity <= 0:
        # Remove item
        await db.carts.update_one(
            {"user_id": user_id},
            {"$pull": {"items": {"product_id": product_id}}}
        )
    else:
        # Update quantity
        await db.carts.update_one(
            {"user_id": user_id, "items.product_id": product_id},
            {"$set": {"items.$.quantity": quantity}}
        )
    
    return await get_cart(user_id)

@router.delete("/items/{product_id}", response_model=CartResponse)
async def remove_from_cart(product_id: str, user_id: str = Depends(get_current_user)):
    db = get_database()
    cart = await db.carts.find_one({"user_id": user_id})
    
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )
    
    await db.carts.update_one(
        {"user_id": user_id},
        {"$pull": {"items": {"product_id": product_id}}}
    )
    
    return await get_cart(user_id)

@router.delete("", response_model=CartResponse)
async def clear_cart(user_id: str = Depends(get_current_user)):
    db = get_database()
    await db.carts.delete_one({"user_id": user_id})
    
    return CartResponse(user_id=user_id, items=[], total_items=0, total_price=0)
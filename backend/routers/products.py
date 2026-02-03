from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models import ProductCreate, ProductUpdate, ProductResponse
from database import get_database
from auth import get_current_user, get_current_admin
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("", response_model=List[ProductResponse])
async def get_products():
    db = get_database()
    products = await db.products.find().to_list(length=100)
    return [
        ProductResponse(
            id=str(product["_id"]),
            name=product["name"],
            description=product["description"],
            price=product["price"],
            category=product["category"],
            stock=product["stock"],
            image=product.get("image", "https://via.placeholder.com/300x300"),
            rating=product.get("rating", 0),
            numReviews=product.get("numReviews", 0),
            created_at=product["created_at"]
        )
        for product in products
    ]

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    db = get_database()
    try:
        product = await db.products.find_one({"_id": ObjectId(product_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return ProductResponse(
        id=str(product["_id"]),
        name=product["name"],
        description=product["description"],
        price=product["price"],
        category=product["category"],
        stock=product["stock"],
        image=product.get("image", "https://via.placeholder.com/300x300"),
        rating=product.get("rating", 0),
        numReviews=product.get("numReviews", 0),
        created_at=product["created_at"]
    )

@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, user_id: str = Depends(get_current_admin)):
    db = get_database()
    product_dict = product.model_dump()
    product_dict["created_at"] = datetime.utcnow()
    product_dict["rating"] = 0
    product_dict["numReviews"] = 0
    
    result = await db.products.insert_one(product_dict)
    created_product = await db.products.find_one({"_id": result.inserted_id})
    
    return ProductResponse(
        id=str(created_product["_id"]),
        name=created_product["name"],
        description=created_product["description"],
        price=created_product["price"],
        category=created_product["category"],
        stock=created_product["stock"],
        image=created_product.get("image", "https://via.placeholder.com/300x300"),
        rating=created_product.get("rating", 0),
        numReviews=created_product.get("numReviews", 0),
        created_at=created_product["created_at"]
    )

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, product_update: ProductUpdate, user_id: str = Depends(get_current_admin)):
    db = get_database()
    try:
        product = await db.products.find_one({"_id": ObjectId(product_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    update_data = {k: v for k, v in product_update.model_dump().items() if v is not None}
    await db.products.update_one({"_id": ObjectId(product_id)}, {"$set": update_data})
    
    updated_product = await db.products.find_one({"_id": ObjectId(product_id)})
    return ProductResponse(
        id=str(updated_product["_id"]),
        name=updated_product["name"],
        description=updated_product["description"],
        price=updated_product["price"],
        category=updated_product["category"],
        stock=updated_product["stock"],
        image=updated_product.get("image", "https://via.placeholder.com/300x300"),
        rating=updated_product.get("rating", 0),
        numReviews=updated_product.get("numReviews", 0),
        created_at=updated_product["created_at"]
    )

@router.delete("/{product_id}")
async def delete_product(product_id: str, user_id: str = Depends(get_current_admin)):
    db = get_database()
    try:
        product = await db.products.find_one({"_id": ObjectId(product_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    await db.products.delete_one({"_id": ObjectId(product_id)})
    return {"message": "Product deleted successfully"}
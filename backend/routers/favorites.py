from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models import FavoriteCreate, FavoriteResponse, ProductResponse
from database import get_database
from auth import get_current_user
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/api/favorites", tags=["Favorites"])

@router.get("", response_model=List[FavoriteResponse])
async def get_favorites(user_id: str = Depends(get_current_user)):
    db = get_database()
    
    favorites = await db.favorites.find({"user_id": user_id}).to_list(length=100)
    
    favorite_responses = []
    for favorite in favorites:
        # Get product details
        product = await db.products.find_one({"_id": ObjectId(favorite["product_id"])})
        if product:
            product_response = ProductResponse(
                id=str(product["_id"]),
                name=product["name"],
                description=product["description"],
                price=product["price"],
                category=product["category"],
                stock=product["stock"],
                image=product.get("image", "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjZjBmMGMwIi8+CjxwYXRoIGQ9Ik0xNTAgMTUwIEMxNzcuNjEgMTUwIDE5NSAxMzIuNjEgMTk1IDEwNSBDMTk1IDc3LjM5IDE3Ny42MSA2MCAxNTAgNjAgQzEyMi4zOSA2MCAxMDUgNzcuMzkgMTA1IDEwNSBDMTA1IDEzMi42MSAxMjIuMzkgMTUwIDE1MCAxNTAiIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4yIi8+Cjx0ZXh0IHg9IjE1MCIgeT0iMTY1IiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiMwMDAiPk5vIEltYWdlPC90ZXh0Pgo8L3N2Zz4="),
                rating=product.get("rating", 0),
                numReviews=product.get("numReviews", 0),
                created_at=product["created_at"]
            )
            
            favorite_responses.append(FavoriteResponse(
                id=str(favorite["_id"]),
                user_id=favorite["user_id"],
                product_id=favorite["product_id"],
                product=product_response,
                created_at=favorite["created_at"]
            ))
    
    return favorite_responses

@router.post("", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
async def add_to_favorites(favorite: FavoriteCreate, user_id: str = Depends(get_current_user)):
    db = get_database()
    
    # Check if product exists
    product = await db.products.find_one({"_id": ObjectId(favorite.product_id)})
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Check if already favorited
    existing_favorite = await db.favorites.find_one({
        "user_id": user_id,
        "product_id": favorite.product_id
    })
    if existing_favorite:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already in favorites"
        )
    
    # Create favorite
    favorite_dict = {
        "user_id": user_id,
        "product_id": favorite.product_id,
        "created_at": datetime.utcnow()
    }
    
    result = await db.favorites.insert_one(favorite_dict)
    created_favorite = await db.favorites.find_one({"_id": result.inserted_id})
    
    # Create product response
    product_response = ProductResponse(
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
    
    return FavoriteResponse(
        id=str(created_favorite["_id"]),
        user_id=created_favorite["user_id"],
        product_id=created_favorite["product_id"],
        product=product_response,
        created_at=created_favorite["created_at"]
    )

@router.delete("/{product_id}")
async def remove_from_favorites(product_id: str, user_id: str = Depends(get_current_user)):
    db = get_database()
    
    result = await db.favorites.delete_one({
        "user_id": user_id,
        "product_id": product_id
    })
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not in favorites"
        )
    
    return {"message": "Product removed from favorites successfully"}

@router.get("/check/{product_id}")
async def check_favorite(product_id: str, user_id: str = Depends(get_current_user)):
    db = get_database()
    
    favorite = await db.favorites.find_one({
        "user_id": user_id,
        "product_id": product_id
    })
    
    return {"is_favorite": favorite is not None}

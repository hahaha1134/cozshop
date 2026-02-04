from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models import ReviewCreate, ReviewResponse
from database import get_database
from auth import get_current_user
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])

@router.get("/product/{product_id}", response_model=List[ReviewResponse])
async def get_product_reviews(product_id: str):
    db = get_database()
    
    # Check if product exists
    product = await db.products.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    reviews = await db.reviews.find({"product_id": product_id}).to_list(length=100)
    reviews.sort(key=lambda x: x["created_at"], reverse=True)
    
    return [
        ReviewResponse(
            id=str(review["_id"]),
            user_id=review["user_id"],
            product_id=review["product_id"],
            rating=review["rating"],
            comment=review["comment"],
            created_at=review["created_at"]
        )
        for review in reviews
    ]

@router.post("", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(review: ReviewCreate, user_id: str = Depends(get_current_user)):
    db = get_database()
    
    # Check if product exists
    product = await db.products.find_one({"_id": ObjectId(review.product_id)})
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Check if user has already reviewed this product
    existing_review = await db.reviews.find_one({
        "user_id": user_id,
        "product_id": review.product_id
    })
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this product"
        )
    
    # Check if user has purchased this product
    has_purchased = await db.orders.find_one({
        "user_id": user_id,
        "items": {
            "$elemMatch": {
                "product_id": review.product_id
            }
        }
    })
    if not has_purchased:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only review products you have purchased"
        )
    
    # Create review
    review_dict = review.model_dump()
    review_dict["user_id"] = user_id
    review_dict["created_at"] = datetime.utcnow()
    
    result = await db.reviews.insert_one(review_dict)
    created_review = await db.reviews.find_one({"_id": result.inserted_id})
    
    # Update product rating and numReviews
    reviews = await db.reviews.find({"product_id": review.product_id}).to_list(length=100)
    total_rating = sum(r["rating"] for r in reviews)
    avg_rating = total_rating / len(reviews)
    
    await db.products.update_one(
        {"_id": ObjectId(review.product_id)},
        {
            "$set": {
                "rating": round(avg_rating, 1),
                "numReviews": len(reviews)
            }
        }
    )
    
    return ReviewResponse(
        id=str(created_review["_id"]),
        user_id=created_review["user_id"],
        product_id=created_review["product_id"],
        rating=created_review["rating"],
        comment=created_review["comment"],
        created_at=created_review["created_at"]
    )

@router.delete("/{review_id}")
async def delete_review(review_id: str, user_id: str = Depends(get_current_user)):
    db = get_database()
    
    try:
        review = await db.reviews.find_one({"_id": ObjectId(review_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    # Check if user is the reviewer
    if review["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this review"
        )
    
    product_id = review["product_id"]
    await db.reviews.delete_one({"_id": ObjectId(review_id)})
    
    # Update product rating and numReviews
    reviews = await db.reviews.find({"product_id": product_id}).to_list(length=100)
    if reviews:
        total_rating = sum(r["rating"] for r in reviews)
        avg_rating = total_rating / len(reviews)
    else:
        avg_rating = 0
    
    await db.products.update_one(
        {"_id": ObjectId(product_id)},
        {
            "$set": {
                "rating": round(avg_rating, 1),
                "numReviews": len(reviews)
            }
        }
    )
    
    return {"message": "Review deleted successfully"}

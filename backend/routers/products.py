from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List, Optional
from models import ProductCreate, ProductUpdate, ProductResponse
from database import get_database
from auth import get_current_user, get_current_admin
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("", response_model=List[ProductResponse])
async def get_products(search: Optional[str] = None, category: Optional[str] = None, min_price: Optional[float] = None, max_price: Optional[float] = None):
    db = get_database()
    
    # Build query
    query = {}
    
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    if category:
        query["category"] = category
    
    if min_price is not None:
        query["price"] = {"$gte": min_price}
    
    if max_price is not None:
        if "price" in query:
            query["price"]["$lte"] = max_price
        else:
            query["price"] = {"$lte": max_price}
    
    products = await db.products.find(query).to_list(length=100)
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

@router.get("/my", response_model=List[ProductResponse])
async def get_my_products(user_id: str = Depends(get_current_user)):
    db = get_database()
    products = await db.products.find({"seller_id": user_id}).to_list(length=100)
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
async def create_product(product: ProductCreate, user_id: str = Depends(get_current_user)):
    db = get_database()
    product_dict = product.model_dump()
    product_dict["created_at"] = datetime.utcnow()
    product_dict["rating"] = 0
    product_dict["numReviews"] = 0
    product_dict["seller_id"] = user_id
    
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
async def update_product(product_id: str, product_update: ProductUpdate, user_id: str = Depends(get_current_user)):
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
    
    # Check if user is the seller or admin
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if product.get("seller_id") != user_id and user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this product"
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
async def delete_product(product_id: str, user_id: str = Depends(get_current_user)):
    db = get_database()
    
    print(f"Delete product request received: product_id={product_id}, user_id={user_id}")
    
    try:
        # Get user to check role
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get all products
        all_products = await db.products.find({}).to_list(length=100)
        print(f"All products count: {len(all_products)}")
        
        # Find the product to delete
        product_to_delete = None
        for product in all_products:
            print(f"  Checking product: {product['name']}, ID: {product['_id']}, Type: {type(product['_id'])}")
            # Check if product ID matches (either as ObjectId or string)
            if str(product['_id']) == product_id:
                product_to_delete = product
                print(f"  Found product to delete: {product['name']}")
                break
        
        if not product_to_delete:
            print(f"Product not found: {product_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        # Check if user is the seller or admin
        seller_id = product_to_delete.get("seller_id")
        user_role = user.get("role")
        print(f"Seller ID: {seller_id}, User ID: {user_id}, User Role: {user_role}")
        
        if seller_id != user_id and user_role != "admin":
            print(f"Not authorized to delete product: seller_id={seller_id}, user_id={user_id}, user_role={user_role}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this product"
            )
        
        # Delete the product
        result = await db.products.delete_one({"_id": product_to_delete["_id"]})
        print(f"Delete result: {result}")
        print(f"Deleted count: {result.deleted_count}")
        
        if result.deleted_count == 0:
            print(f"No product deleted: {product_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        print(f"Product deleted successfully: {product_id}")
        return {"message": "Product deleted successfully"}
    except Exception as e:
        print(f"Error deleting product: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting product: {str(e)}"
        )

@router.put("/{product_id}/status")
async def update_product_status(product_id: str, status_data: dict = Body(..., description="状态数据"), user_id: str = Depends(get_current_admin)):
    db = get_database()
    
    status = status_data.get("status")
    valid_statuses = ["pending", "approved", "rejected", "inactive"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    try:
        result = await db.products.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": {"status": status}}
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return {"message": "Product status updated successfully"}

@router.put("/{product_id}/pin")
async def update_product_pin(product_id: str, pin_data: dict = Body(..., description="置顶数据"), user_id: str = Depends(get_current_admin)):
    db = get_database()
    
    is_pinned = pin_data.get("is_pinned", False)
    
    try:
        # Try to convert product_id to ObjectId
        product_object_id = ObjectId(product_id)
        print(f"Product ID: {product_id}")
        print(f"ObjectId: {product_object_id}")
        
        # First check if product exists
        product = await db.products.find_one({"_id": product_object_id})
        print(f"Product found: {product}")
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        # Update product pin status
        result = await db.products.update_one(
            {"_id": product_object_id},
            {"$set": {"is_pinned": is_pinned}}
        )
        
        print(f"Update result: {result}")
        
        # Check if product exists (matched_count > 0 if product was found)
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        return {"message": "Product pin status updated successfully"}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {str(e)}"
        )
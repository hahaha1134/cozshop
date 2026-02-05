from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List, Optional
from models import UserResponse
from database import get_database
from auth import get_current_admin, get_current_user
from bson import ObjectId

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("", response_model=List[UserResponse])
async def get_all_users(user_id: str = Depends(get_current_admin)):
    db = get_database()
    users = await db.users.find().to_list(length=100)
    
    return [
        UserResponse(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            role=user.get("role", "user"),
            created_at=user["created_at"]
        )
        for user in users
    ]

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, admin_id: str = Depends(get_current_admin)):
    db = get_database()
    try:
        user = await db.users.find_one({"_id": ObjectId(user_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=str(user["_id"]),
        name=user["name"],
        email=user["email"],
        role=user.get("role", "user"),
        created_at=user["created_at"]
    )

@router.put("/{user_id}/role")
async def update_user_role(user_id: str, role: str, admin_id: str = Depends(get_current_admin)):
    db = get_database()
    
    if role not in ["user", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role. Must be either 'user' or 'admin'"
        )
    
    try:
        result = await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"role": role}}
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User role updated successfully"}

@router.delete("/{user_id}")
async def delete_user(user_id: str, admin_id: str = Depends(get_current_admin)):
    db = get_database()
    
    try:
        result = await db.users.delete_one({"_id": ObjectId(user_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User deleted successfully"}

@router.put("/{user_id}/status")
async def update_user_status(user_id: str, status: str, admin_id: str = Depends(get_current_admin)):
    db = get_database()
    
    if status not in ["active", "inactive"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status. Must be either 'active' or 'inactive'"
        )
    
    try:
        result = await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"status": status}}
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User status updated successfully"}

@router.put("/profile/update")
async def update_profile(
    name: Optional[str] = Body(None, description="用户名"),
    phone: Optional[str] = Body(None, description="手机号"),
    address: Optional[str] = Body(None, description="收货地址"),
    user_id: str = Depends(get_current_user)
):
    db = get_database()
    
    # Prepare update data
    update_data = {}
    if name:
        update_data["name"] = name
    if phone:
        update_data["phone"] = phone
    if address:
        update_data["address"] = address
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided for update"
        )
    
    try:
        result = await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get updated user
    updated_user = await db.users.find_one({"_id": ObjectId(user_id)})
    
    return {
        "message": "Profile updated successfully",
        "user": UserResponse(
            id=str(updated_user["_id"]),
            name=updated_user["name"],
            email=updated_user["email"],
            role=updated_user.get("role", "user"),
            created_at=updated_user["created_at"]
        )
    }

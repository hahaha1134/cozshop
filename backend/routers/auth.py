from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from models import UserCreate, UserResponse, Token, UserLogin
from database import get_database
from auth import get_current_user
from bson import ObjectId

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    db = get_database()
    
    # Check if user exists
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user (no password hashing)
    user_dict = user.model_dump()
    user_dict["role"] = "user"
    user_dict["created_at"] = datetime.utcnow()
    
    result = await db.users.insert_one(user_dict)
    created_user = await db.users.find_one({"_id": result.inserted_id})
    
    # Simplified: use user_id as token
    access_token = str(created_user["_id"])
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=str(created_user["_id"]),
            name=created_user["name"],
            email=created_user["email"],
            role=created_user["role"],
            created_at=created_user["created_at"]
        )
    )

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    db = get_database()
    
    # Simplified: no password verification
    user_data = await db.users.find_one({"email": user.email})
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Simplified: use user_id as token
    access_token = str(user_data["_id"])
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=str(user_data["_id"]),
            name=user_data["name"],
            email=user_data["email"],
            role=user_data["role"],
            created_at=user_data["created_at"]
        )
    )

@router.get("/profile", response_model=UserResponse)
async def get_profile(user_id: str = Depends(get_current_user)):
    db = get_database()
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse(
        id=str(user["_id"]),
        name=user["name"],
        email=user["email"],
        role=user["role"],
        created_at=user["created_at"]
    )
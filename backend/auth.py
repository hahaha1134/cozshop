from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        # 尝试使用哈希验证
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        # 如果哈希验证失败，尝试直接比较明文密码（向后兼容）
        return plain_password == hashed_password

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Simplified: use token directly as user_id
    user_id = credentials.credentials
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    from database import get_database
    from bson import ObjectId
    db = get_database()
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if user.get("status") == "inactive":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account has been disabled",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_id

async def get_current_admin(user_id: str = Depends(get_current_user)):
    from database import get_database
    from bson import ObjectId
    db = get_database()
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if user and user.get("role") == "admin":
        return user_id
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not enough permissions"
    )
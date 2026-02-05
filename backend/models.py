from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# 定义默认的占位图片（base64 编码的 SVG）
DEFAULT_IMAGE = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjZjBmMGMwIi8+CjxwYXRoIGQ9Ik0xNTAgMTUwIEMxNzcuNjEgMTUwIDE5NSAxMzIuNjEgMTk1IDEwNSBDMTk1IDc3LjM5IDE3Ny42MSA2MCAxNTAgNjAgQzEyMi4zOSA2MCAxMDUgNzcuMzkgMTA1IDEwNSBDMTA1IDEzMi42MSAxMjIuMzkgMTUwIDE1MCAxNTAiIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4yIi8+Cjx0ZXh0IHg9IjE1MCIgeT0iMTY1IiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiMwMDAiPk5vIEltYWdlPC90ZXh0Pgo8L3N2Zz4="

# User Models
class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = ""
    address: Optional[str] = ""

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: str
    role: str = "user"
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Product Models
class ProductBase(BaseModel):
    name: str
    description: str
    price: float = Field(..., gt=0)
    category: str
    stock: int = Field(..., ge=0)
    image: Optional[str] = DEFAULT_IMAGE

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    stock: Optional[int] = None
    image: Optional[str] = None
    rating: Optional[float] = None
    numReviews: Optional[int] = None

class ProductResponse(ProductBase):
    id: str
    rating: float = 0
    numReviews: int = 0
    created_at: datetime
    status: Optional[str] = "pending"
    seller_id: Optional[str] = None

    class Config:
        from_attributes = True

# Cart Models
class CartItem(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int = Field(..., gt=0)
    image: Optional[str] = DEFAULT_IMAGE

class CartResponse(BaseModel):
    user_id: str
    items: List[CartItem]
    total_items: int
    total_price: float

    class Config:
        from_attributes = True

# Order Models
class ShippingAddress(BaseModel):
    address: Optional[str] = ""
    city: Optional[str] = ""
    postalCode: Optional[str] = ""
    country: Optional[str] = ""

class OrderItem(BaseModel):
    name: str
    quantity: int
    image: Optional[str] = DEFAULT_IMAGE
    price: float
    product_id: str

class OrderCreate(BaseModel):
    shippingAddress: ShippingAddress
    paymentMethod: str

class OrderResponse(BaseModel):
    id: str
    user_id: str
    orderItems: List[OrderItem]
    shippingAddress: Optional[ShippingAddress] = ShippingAddress()
    paymentMethod: Optional[str] = ""
    itemsPrice: Optional[float] = 0
    taxPrice: Optional[float] = 0
    shippingPrice: Optional[float] = 0
    totalPrice: float
    status: str = "pending"
    paidAt: Optional[datetime] = None
    deliveredAt: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Review Models
class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: str

class ReviewCreate(ReviewBase):
    product_id: str

class ReviewResponse(ReviewBase):
    id: str
    user_id: str
    product_id: str
    created_at: datetime

    class Config:
        from_attributes = True

# Favorite Models
class FavoriteBase(BaseModel):
    product_id: str

class FavoriteCreate(FavoriteBase):
    pass

class FavoriteResponse(BaseModel):
    id: str
    user_id: str
    product_id: str
    product: ProductResponse
    created_at: datetime

    class Config:
        from_attributes = True

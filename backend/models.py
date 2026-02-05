from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

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
    image: Optional[str] = "https://via.placeholder.com/300x300"

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

    class Config:
        from_attributes = True

# Cart Models
class CartItem(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int = Field(..., gt=0)
    image: Optional[str] = "https://via.placeholder.com/300x300"

class CartResponse(BaseModel):
    user_id: str
    items: List[CartItem]
    total_items: int
    total_price: float

    class Config:
        from_attributes = True

# Order Models
class ShippingAddress(BaseModel):
    address: str
    city: str
    postalCode: str
    country: str

class OrderItem(BaseModel):
    name: str
    quantity: int
    image: str
    price: float
    product_id: str

class OrderCreate(BaseModel):
    shippingAddress: ShippingAddress
    paymentMethod: str

class OrderResponse(BaseModel):
    id: str
    user_id: str
    orderItems: List[OrderItem]
    shippingAddress: ShippingAddress
    paymentMethod: str
    itemsPrice: float
    taxPrice: float
    shippingPrice: float
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
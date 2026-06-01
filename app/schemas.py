#====SCHEMA DEFINITIONS====#
from pydantic import BaseModel
from pydantic import EmailStr, conint
from typing import Optional 

# Schema for user signup request
class UserSignup(BaseModel):
    username: str
    email: EmailStr
    phone: str
    password: str

#user response schema
class UserSignupResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone: str

    class Config:
        orm_mode = True

# Schema for user signup response
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for product creation request
class ProductCreate(BaseModel):
    name: str
    description: str
    price: int
    stock: int

# Schema for product response
class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: int
    stock: int
    status: str
    rating: Optional[int] = None
    review: Optional[str] = None
    is_available: bool

    class Config:
        from_attributes = True

#schema for cart
class CartAdd(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

#response model for cart
class CartResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    class config:
        orm_mode = True

class ProductRating(BaseModel):
    post_id: int
    rating: int = [i for i in range(0, 5)]
    review: str


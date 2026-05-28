#====SCHEMA DEFINITIONS====#
from pydantic import BaseModel
from pydantic import EmailStr 

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

# Schema for product response
class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: int
    is_available: bool

    class Config:
        orm_mode = True
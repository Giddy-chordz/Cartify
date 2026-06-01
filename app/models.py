#===SETUP DATABASE MODELS===#
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from .database import Base
import datetime

#create user model
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(String, default=datetime.datetime.utcnow)

#setup product model
class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Integer)
    stock = Column(Integer, default=0)
    status = Column(String, default="available") # available, out of stock, discontinued
    is_available = Column(Boolean, default=True)# 1 for available, 0 for not available
    created_at = Column(String, default=datetime.datetime.utcnow)

#setup order model
class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer)
    quantity = Column(Integer)
    total_price = Column(Integer)
    created_at = Column(String, default=datetime.datetime.utcnow)

#setup cart model
class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer)
    created_at = Column(String, default=datetime.datetime.utcnow)

class ProductRating(Base):
    __tablename__ = 'product_ratings'
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key = True, nullable=False)
    rating = Column(Integer) # ranges from 0 to 5
    review = Column(String)
    created_at = Column(String, default=datetime.datetime.utcnow)
#===SETUP DATABASE MODELS===#
from sqlalchemy import Column, Integer, String, Boolean
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
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Integer)
    is_available = Column(Boolean, default=True)# 1 for available, 0 for not available
    created_at = Column(String, default=datetime.datetime.utcnow)

#setup order model
class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    product_id = Column(Integer)
    quantity = Column(Integer)
    total_price = Column(Integer)
    created_at = Column(String, default=datetime.datetime.utcnow)

#setup cart model
class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    product_id = Column(Integer)
    quantity = Column(Integer)
    created_at = Column(String, default=datetime.datetime.utcnow)
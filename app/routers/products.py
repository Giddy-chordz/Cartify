from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from ..models import Products
from ..oauth2 import get_current_user
from ..schemas import ProductCreate, ProductResponse

#instantiate router
router = APIRouter(tags = ['add products'])

@router.post("/add", response_model = ProductResponse)
def add_product(products: ProductCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    #allow users to add products
    new_product = Products(**products.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

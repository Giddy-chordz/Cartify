from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from ..models import Products
from ..oauth2 import get_current_user, verify_admin_user
from ..schemas import ProductCreate, ProductRating, ProductResponse
from typing import Optional
from .vote_query import rating_query

#instantiate router
router = APIRouter(tags = ['products'])

@router.post("/add", response_model = ProductResponse)
def add_product(products: ProductCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user), admin_user: str = Depends(verify_admin_user)):
    #allow users to add products
    new_product = Products(**products.model_dump(), owner_id = current_user.id, status = 'available')
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@router.get("/", response_model = list[ProductResponse])
def get_products(db: Session = Depends(get_db), search: Optional[str] = ""):

    #get all products
    all_products = db.query(Products).filter(Products.name.contains(search)).all()

    #get ratings for each product and include it in the response
    products_with_ratings = []
    for product in all_products:
        rating = rating_query(db, product.id)
        product_data = ProductResponse.model_validate(product)
        if rating:
            product_data.rating = rating.rating
            product_data.review = rating.review
        else:
            product_data.rating = None
            product_data.review = None
        products_with_ratings.append(product_data)

    #if stock is 0, set is_available to false, and if stock is greater than 0, set is_available to true
    if all_products:
        for product in all_products:
            if product.stock == 0:
                product.is_available = False
            else:
                product.is_available = True

    return products_with_ratings

#get a single product by id or by search keyword
@router.get("/items/{id}", response_model = ProductResponse)
def get_product(id: int, db: Session = Depends(get_db)):
    #get a single product by id
    product = db.query(Products).filter(Products.id == id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} not found")

    #if stock is 0, set is_available to false, and if stock is greater than 0, set is_available to true
    if product.stock == 0:
        product.is_available = False
        product.status = 'out_of_stock'
    else:
        product.is_available = True
        product.status = 'available'
    return product


#delete a product by id
@router.delete("/delete/{id}")
def delete_product(id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user), admin_user: str = Depends(verify_admin_user)):
    #delete a product by id
    product_query = db.query(Products).filter(Products.id == id)

    product = product_query.first()
    #raise an error if the product does not exist
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} not found")

    db.delete(synchronize_session=False)
    db.commit()

    #enable owner of products to delete their products
    if product.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to delete this product")
    
    #enable admin users to delete any product
    if admin_user.role == 'admin':
        db.delete(product)
        db.commit()

    return {"detail": f"Product with id {id} deleted successfully"}
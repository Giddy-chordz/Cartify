from fastapi import FastAPI, APIRouter, status, HTTPException, Depends 
from sqlalchemy.orm import Session, Session
from ..database import get_db
from ..models import Cart, Products
from ..schemas import CartAdd, CartResponse
from ..oauth2 import get_current_user
from .. import utils

router = APIRouter(prefix = "/cart",
                   tags = ["cart"])

#allow users to add product to cart

@router.post("/add", response_model = CartResponse, status_code = status.HTTP_201_CREATED)
def add_to_cart(cart: CartAdd, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    #allow users to add product to cart
    product = db.query(Products).filter(Products.id == cart.product_id).first()
    
    #raise an error if user is not logged in
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You must be logged in to add items to cart")
    
    #raise an error if product does not exists
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {cart.product_id} not found")
    new_cart_item = Cart(**cart.model_dump(), user_id = current_user.id)

    #to ensure users dont add more than available products
    if cart.quantity > product.stock:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Only {product.stock} items available in stock")
    
    #when a user adds a product_id to cart multiple times, it should update the quantity of the existing cart item instead of creating a new cart item
    existing_cart_item = db.query(Cart).filter(Cart.user_id == current_user.id, Cart.product_id == cart.product_id).first()
    if existing_cart_item:
        existing_cart_item.quantity += cart.quantity

        #to ensure users dont add more than available products
        if existing_cart_item.quantity > product.stock:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Only {product.stock} items available in stock")
        
        db.commit()
        db.refresh(existing_cart_item)
        return existing_cart_item
    
    db.add(new_cart_item)
    db.commit()
    db.refresh(new_cart_item)

    return  new_cart_item

#get all items in cart
@router.get("/", response_model = list[CartResponse])
def get_cart_items(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    #get all items in cart
    cart_items = db.query(Cart).filter(Cart.user_id == current_user.id).all()

    #to display name of the product in the cart response, we can use the product_id to query the Products table and get the name of the product, then include it in the cart response
    for item in cart_items:
        product = db.query(Products).filter(Products.id == item.product_id).first()
        item.product_name = product.name

    return cart_items

#delete an item from cart by id
@router.delete("/delete/{id}")
def delete_cart_item(id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    #delete an item from cart by id
    cart_item_query = db.query(Cart).filter(Cart.id == id)

    cart_item = cart_item_query.first()
    #raise an error if the cart item does not exist
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cart item with id {id} not found")
    
    
    #raise an error if the cart item does not belong to the current user
    if cart_item.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this cart item")

    db.delete(cart_item)
    db.commit()

    return {"detail": f"Cart item with id {id} deleted successfully"}
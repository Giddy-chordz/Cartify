from fastapi import FastAPI, APIRouter, status, HTTPException, Depends 
from sqlalchemy.orm import Session, Session
from ..database import get_db
from ..models import Cart
from ..schemas import CartAdd, CartResponse
from ..oauth2 import get_current_user
from .. import utils

router = APIRouter(prefix = "cart",
                   tags = "cart")

#allow users to add product to cart

@router.post("/add", response_model = CartResponse, status_code = status.HTTP_201_CREATED)
def add_to_cart(cart: CartAdd, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    #allow users to add product to cart
    new_cart_item = Cart(**cart.model_dump(), user_id = current_user.id)
    db.add(new_cart_item)
    db.commit()
    db.refresh(new_cart_item)

    return new_cart_item

#get all items in cart
@router.get("/", response_model = list[CartResponse])
def get_cart_items(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    #get all items in cart
    cart_items = db.query(Cart).filter(Cart.user_id == current_user.id).all()

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

    db.delete(synchronize_session=False)
    db.commit()

    return {"detail": f"Cart item with id {id} deleted successfully"}
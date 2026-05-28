#====SETUP USER AUTHENTICATION ROUTES====#
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, utils, oauth2
from ..schemas import UserSignup, UserSignupResponse, Token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

#=== USER SIGNUP ENDPOINT ===#
@router.post("/signup", response_model=UserSignupResponse, status_code=status.HTTP_201_CREATED)
def sign_up(user: UserSignup, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.query(models.Users).filter(models.Users.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    # Hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    # Create a new user instance
    new_user = models.Users(username = user.username,
                            email = user.email,
                            phone = user.phone,
                            password = user.password)

    # Add the new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
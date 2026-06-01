#===== CREATE ACCESS TOKEN FUNCTION =====#
from jose import JWTError, jwt
from datetime import datetime, timedelta
import secrets
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from . import models
from .database import get_db
from sqlalchemy.orm import Session
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = SECRET_KEY
ALGORITHM = ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES

#function to create an access token: this function takes a dictionary of data 
#(usually containing the user's ID) and creates a JWT access token that includes 
# the data and an expiration time. The token is signed using the SECRET_KEY and ALGORITHM 
# defined above, ensuring that it can be verified later when the user makes requests to 
# protected endpoints.
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return access_token
#verify access token function: this function takes a JWT token and a credentials_exception as
#  parameters. It attempts to decode the token using the SECRET_KEY and ALGORITHM. If the token 
# is valid and not expired, it extracts the user ID from the token's payload and returns it. 
# If the token is invalid or expired, it raises the provided credentials_exception, which 
# typically results in a 401 Unauthorized response when used in protected endpoints.
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

        return user_id

    except JWTError:
        raise credentials_exception
    
# Define the OAuth2 scheme for token extraction: this creates an instance of the
#  OAuth2PasswordBearer class, which is used to extract the token from the Authorization 
# header of incoming requests. The tokenUrl parameter specifies the URL where clients can 
# obtain a token (in this case, "/auth/login"). This scheme will be used as a dependency in 
# protected endpoints to automatically handle token extraction and validation.

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)
    
    user = db.query(models.Users).filter(models.Users.id == token).first()

    return user
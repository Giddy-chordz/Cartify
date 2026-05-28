#===== CREATE ACCESS TOKEN FUNCTION =====#
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#function to create an access token: this function takes a dictionary of data 
#(usually containing the user's ID) and creates a JWT access token that includes 
# the data and an expiration time. The token is signed using the SECRET_KEY and ALGORITHM 
# defined above, ensuring that it can be verified later when the user makes requests to 
# protected endpoints.
def create_access_token(data: dict):
    to_encode = data.copy()

#====PASSWORD HASHING UTILS====#
from passlib.context import CryptContext

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

# Function to verify a plain password against a hashed password
def verify(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
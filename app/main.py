from fastapi import FastAPI
from .database import engine, get_db
from . import models, config
from .routers import auth, products, carts
from fastapi.middleware.cors import CORSMiddleware

#create tables defined in models.py in the database
models.Base.metadata.create_all(bind = engine)

app = FastAPI()

#setup CORS middleware to allow requests from the frontend application running on localhost:3000
origins = ["http://localhost:3000"]
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



#include the authentication router
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(carts.router)
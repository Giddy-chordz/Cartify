from fastapi import FastAPI
from .database import engine, get_db
from . import models, config
from .routers import auth, products, carts


app = FastAPI()

#create tables defined in models.py in the database
models.Base.metadata.create_all(bind = engine)

#include the authentication router
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(carts.router)
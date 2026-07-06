from fastapi import FastAPI, Depends, HTTPException, status 
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas , utils
from .database import engine, get_db
from .routers import user , post

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



app.include_router(post.router)
app.include_router(user.router)



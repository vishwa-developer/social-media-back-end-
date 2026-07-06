from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Get all posts
@app.get("/posts", response_model=List[schemas.Post])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# Get one post
@app.get("/posts/{id}", response_model=schemas.Post)
def get_one_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )

    return post


# Create post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(
        title=post.title,
        content=post.content,
        published=post.published
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# Delete post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return


# Update post
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.CreatePost,
    db: Session = Depends(get_db)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()


# Get all users
@app.get("/users", response_model=List[schemas.User])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.users).all()
    return users


# Get one user
@app.get("/users/{id}", response_model=schemas.User)
def get_one_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.users).filter(models.users.id == id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} was not found"
        )

    return user


# Create user
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.users(
        email=user.email,
        password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
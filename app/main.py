from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import models,schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()




# Get all posts
@app.get("/posts")
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# Get single post
@app.get("/posts/{id}")
def get_one_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )

    return post


# Create post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.createPost, db: Session = Depends(get_db)):
    new_post = models.Post(
        title=post.title,
        content=post.content,
        published=post.published
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return  new_post


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
@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.createPost, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )

    post_query.update(updated_post.model_dump(), synchronize_session=False)

    db.commit()

    return  post_query.first()
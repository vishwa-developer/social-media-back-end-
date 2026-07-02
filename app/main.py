from fastapi import FastAPI,Response,HTTPException,status,Depends
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .import models
from .database import engine , get_db


models.Base.metadata.create_all(bind=engine)






app = FastAPI()

class post(BaseModel):
    title: str
    content: str
    published: bool=True

#connnecting the database 
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="Vishwa@2004",
            cursor_factory=RealDictCursor
        )

        cursor = conn.cursor()
        print("Database Connected Successfully")
        break

    except Exception as error:
        print("Connection Failed:", error)
        time.sleep(2)

#get all posts 
@app.get("/posts")
def get_all_post():
    cursor.execute("SELECT * FROM public.post;")
    show = cursor.fetchall()
    return {"data": show}

#get a specific post
@app.get("/posts/{id}")
def get_one(id: int):
    cursor.execute(
        "SELECT * FROM public.post WHERE id = %s",
        (id,)
    )

    post = cursor.fetchone()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )

    return {"data": post}


#create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def new_post(post: post):
    cursor.execute(
        """
        INSERT INTO public.post (title, content, published)
        VALUES (%s, %s, %s)
        RETURNING *
        """,
        (post.title, post.content, post.published)
    )

    new_post = cursor.fetchone()
    conn.commit()

    return {"data": new_post}

#delete the post
@app.delete("/posts/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: int):
    cursor.execute(
        """
        DELETE FROM public.post
        WHERE id = %s
        RETURNING *
        """,
        (id,)
    )

    deleted_post = cursor.fetchone()

    conn.commit()

    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )

    return {"data": deleted_post}

#update the post
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: post):
    cursor.execute(
        """
        UPDATE public.post
        SET title = %s,
            content = %s,
            published = %s
        WHERE id = %s
        RETURNING *
        """,
        (post.title, post.content, post.published, id)
    )

    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )

    return {"data": updated_post}

@app.get("/sql")
def get_database(db: Session = Depends(get_db)):
    post=db.query(models.Post).all()
    return {'data': post }







   
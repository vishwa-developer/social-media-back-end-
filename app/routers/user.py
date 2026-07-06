from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import schemas, models, utils


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# Get all users
@router.get("/", response_model=List[schemas.User])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.users).all()
    return users


# Get one user
@router.get("/{id}", response_model=schemas.User)
def get_one_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.users).filter(models.users.id == id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} was not found"
        )

    return user


# Create user
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.User
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)

    new_user = models.users(
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
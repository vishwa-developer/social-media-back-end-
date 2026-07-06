from fastapi import APIRouter,Depends,HTTPException,responses,status
from sqlalchemy.orm import Session
from ..import database , utils ,models,schemas



router=APIRouter(
    tags=["authentication"]
)


@router.post("/login")
def login(user_credentials: schemas.UserCreate,
          db: Session = Depends(database.get_db)):

    user = db.query(models.users).filter(
        models.users.email == user_credentials.email
    ).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )

    return {"message": "Login successful"}
    
    
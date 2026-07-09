from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, models, oauth2, utils, schemas

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):

    # Find user by email
    user = db.query(models.users).filter(
        models.users.email == user_credentials.username
    ).first()

    # Check if user exists
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    # Verify password
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    # Create JWT token
    access_token = oauth2.create_access_token(
        data={"id": user.id}
    )

    # Return token
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
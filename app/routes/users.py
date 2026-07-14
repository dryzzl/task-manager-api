from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import hash_password
from app.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    #--------------------------------
    #Check if username already exists
    #--------------------------------
    existing_username = (
        db.query(models.User)
        .filter(models.User.username == user.username)
        .first()
    )

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )
    
    #--------------------------------
    #Check if email already exists
    #--------------------------------
    existing_email = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )
    #--------------------------------
    # Create the new user
    #--------------------------------
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    #--------------------------------
    # Save to the database
    #--------------------------------
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
from fastapi import APIRouter, Depends,  status, HTTPException
from sqlalchemy.orm import Session
from ...database import get_db
from . import models, Schema
from app.utils import utils
from app.modules.oauth2 import oauth2_router

router = APIRouter(prefix="/users", 
                   tags=['User'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Schema.UserOut)
async def signup(user:Schema.UserCreate, db:Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    user_dict = user.dict()

    # Check if this is the first user - if so, make them admin
    existing_users_count = db.query(models.User).count()
    user_dict['is_admin'] = existing_users_count == 0  # First user becomes admin

    new_user = models.User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=Schema.UserOut)
async def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Id {id} not availabe")
    return user

@router.put("/{id}/promote", status_code=status.HTTP_200_OK, response_model=Schema.UserOut)
async def promote_to_admin(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2_router.get_current_user)
):
    # Check if current user is admin
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can promote other users to admin"
        )

    # Find the user to promote
    user_to_promote = db.query(models.User).filter(models.User.id == id).first()
    if not user_to_promote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )

    # Check if user is already admin
    if user_to_promote.is_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already an admin"
        )

    # Promote user to admin
    user_to_promote.is_admin = True
    db.commit()
    db.refresh(user_to_promote)
    return user_to_promote


    


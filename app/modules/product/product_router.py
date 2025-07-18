from typing import List
from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session

from app.modules.oauth2 import oauth2_router
from ...database import get_db
from . import models
from . import Schema
from app.modules.user import models as user_models

router = APIRouter(prefix="/posts",
                   tags=['Products'])

@router.get("/", response_model=List[Schema.Post])
async def get_all_posts(db: Session = Depends(get_db),
                        current_user:user_models.User = Depends(oauth2_router.get_current_user)):
    post = db.query(models.Product).all()
    return post

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(post: Schema.PostCreate, db: Session = Depends(get_db),
                current_user:user_models.User  = Depends(oauth2_router.get_current_user)):
    new_post = models.Product(**post.dict(), owner_id = current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=Schema.Post)
async def get_single_post(id:int, db: Session = Depends(get_db),
                          current_user:user_models.User  = Depends(oauth2_router.get_current_user)):
    post = db.query(models.Product).filter(models.Product.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Id {id} was not found")
    return post

@router.put("/{id}")
async def updated_post(id:int, update_post:Schema.PostBase, db:Session = Depends(get_db),
                    current_user:user_models.User  = Depends(oauth2_router.get_current_user)):
    post_query= db.query(models.Product).filter(models.Product.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Id {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    post_query.update(update_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleted_post(id:int, db:Session= Depends(get_db),
                    current_user:user_models.User = Depends(oauth2_router.get_current_user)):
    post_query= db.query(models.Product).filter(models.Product.id == id)
    post= post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Id {id}  was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
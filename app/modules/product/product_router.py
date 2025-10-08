from fastapi import APIRouter, Depends, Response, status, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.modules.oauth2 import oauth2_router
from ...database import get_db
from . import models
from . import Schema
from app.modules.user import models as user_models
from app.modules.image import models as image_models
from app.modules.category import models as category_models


router = APIRouter(prefix="/posts",
                   tags=['Products'])



# Searching for products
@router.get("/", response_model=List[Schema.Product])
async def search_products(
    q: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(models.Product)
    if q:
        query = query.filter(models.Product.name == q).limit(1)
    return query.all()




@router.get("")
async def get_all_products(db: Session = Depends(get_db)):
    post = db.query(models.Product).all()
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Schema.Product)
async def create_product(post: Schema.ProductCreate, db: Session = Depends(get_db),
                current_user:user_models.User  = Depends(oauth2_router.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin users can create products.")
    # Check if image exists
    existing_image = db.query(image_models.Image).filter(image_models.Image.id == post.image_id).first()
    if not existing_image:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Image with id {post.image_id} does not exist.")
    # Check if category exists
    existing_category = db.query(category_models.Category).filter(category_models.Category.id == post.category_id).first()
    if not existing_category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Category with id {post.category_id} does not exist.")
    # Check for duplicate product name
    existing_product = db.query(models.Product).filter(models.Product.name == post.name).first()
    if existing_product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product with name {post.name} already exists.")
    new_post = models.Product(**post.dict(), owner_id = current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{name}", response_model=Schema.Product)
async def get_product_by_name(name:str, db: Session = Depends(get_db)):
    post = db.query(models.Product).filter(models.Product.name == name).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with name {name} was not found")
    return post

@router.put("/{id}", response_model=Schema.Product)
async def updated_product(id: int, update_post: Schema.ProductBase, db: Session = Depends(get_db),
                          current_user: user_models.User = Depends(oauth2_router.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    post_query = db.query(models.Product).filter(models.Product.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Id {id} was not found")
    if not (current_user.is_admin or post.owner_id == current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    # Validate image_id if provided
    if update_post.image_id is not None:
        if update_post.image_id == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image_id: cannot be 0")
        existing_image = db.query(image_models.Image).filter(image_models.Image.id == update_post.image_id).first()
        if not existing_image:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Image with id {update_post.image_id} does not exist.")

    # Validate category_id if provided
    if update_post.category_id is not None:
        if update_post.category_id == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category_id: cannot be 0")
        existing_category = db.query(category_models.Category).filter(category_models.Category.id == update_post.category_id).first()
        if not existing_category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Category with id {update_post.category_id} does not exist.")

    # Update only provided fields
    update_data = update_post.dict(exclude_unset=True)
    post_query.update(update_data, synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleted_product(id:int, db:Session= Depends(get_db),
                    current_user:user_models.User = Depends(oauth2_router.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    post_query= db.query(models.Product).filter(models.Product.id == id)
    post= post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Id {id}  was not found")
    if not (current_user.is_admin or post.owner_id == current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

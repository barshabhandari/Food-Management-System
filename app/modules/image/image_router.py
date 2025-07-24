import os
from datetime import datetime
from fastapi import APIRouter, Depends, status, UploadFile, HTTPException
from sqlalchemy.orm import Session
from ...database import get_db
from . import models, Schema
from app.modules.oauth2.oauth2_router import get_current_user
from app.modules.user.models import User

router = APIRouter(prefix="/images", tags=['Image'])

ALLOWED_EXTENSIONS = {"image/png", "image/jpeg", "image/jpg"}
UPLOAD_DIR = "static"

os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure the static directory exists

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Schema.ImageBase)
async def upload_image(image: UploadFile, db: Session = Depends(get_db),
current_user: User = Depends(get_current_user)):
    if image.content_type not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid image format. Only PNG and JPEG are allowed.")

    # Generate a unique key using timestamp
    ext = os.path.splitext(image.filename)[1] or ".png"
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    unique_key = f"{timestamp}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_key)

    # Save the file
    with open(file_path, "wb") as buffer:
        content = await image.read()
        buffer.write(content)

    # Save metadata to DB
    image_record = models.Image(key=unique_key)
    db.add(image_record)
    db.commit()
    db.refresh(image_record)

    return image_record

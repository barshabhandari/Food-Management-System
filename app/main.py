from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import engine
from app.modules.product import models
from app.modules.product.product_router import router as product_router
from app.modules.user.user_router import router as user_router
from app.modules.auth.auth_router import router as auth_router
from app.modules.image.image_router import router as image_router
from fastapi.middleware.cors import CORSMiddleware
from app.modules.category.category_router import router as category_router

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

models.Base.metadata.create_all(bind=engine)


app.include_router(product_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(image_router)
app.include_router(category_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

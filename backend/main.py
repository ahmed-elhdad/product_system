from fastapi import FastAPI
from src.routes import base_router, product_router
from src.config import connect_mongodb
from fastapi.staticfiles import StaticFiles
import os
from fastapi.middleware.cors import CORSMiddleware
import shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # في الإنتاج حدد الدومين بتاعك بدل "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
os.makedirs("uploads/products", exist_ok=True)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.state.db_client = connect_mongodb()
app.include_router(base_router)
app.include_router(product_router)

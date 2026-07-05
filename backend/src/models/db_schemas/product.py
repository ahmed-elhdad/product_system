from .conversation import ConfigDict, PyObjectId
from typing import Optional, List
import datetime
from pydantic import BaseModel, EmailStr, Field, constr
from fastapi import UploadFile, File, Form


class Product(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    title: str = Form(...)
    description: Optional[str] = None
    stock: int = Form(...)
    category: str = Form(...)
    price: int = Form(...)
    discount: int = Form(...)
    images: List[UploadFile] = File(...)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

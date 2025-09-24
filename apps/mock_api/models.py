from pydantic import BaseModel, EmailStr, Field
from typing import List

class UserCreate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr

class User(UserCreate):
    id: int

class OrderItem(BaseModel):
    sku: str
    qty: int = Field(ge=1)

class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItem]

class Order(OrderCreate):
    id: int
    total: float
